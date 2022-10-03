import logging
import socket
import struct

import lib.constants as const
from lib.protocols.base_protocol import BaseProtocol
import lib.segments.RDTPSegment as protocol
import lib.segments.headers.RDTPHeader as rdtp_header
from lib.protocols.base_protocol import LostConnectionError


class GoBackN(BaseProtocol):
    def __init__(self, socket):
        super().__init__(socket, False)
        socket.setblocking(False)
        self.window_size = 10
        self.messages_not_acked = []

    def send(self, data, attempts=0):
        """
        Send data through the socket, creating the necessary headers.
        If an ACK is not received, the packet is added to the in-flight list.
        If the in-flight list is full, awaits ACKs for packages in the list.
        """
        if attempts >= const.TIMEOUT_RETRY_ATTEMPTS:
            self.finished = True
            raise LostConnectionError("Lost connection error")

        # Create packet
        sent = False

        # If the window isnt full, send packet
        if len(self.messages_not_acked) < self.window_size:
            self.seq_num += 1
            head = rdtp_header.RDTPHeader(
                seq_num=self.seq_num, ack_num=self.ack_num, fin=False)
            message = protocol.RDTPSegment(data=data, header=head)

            logging.debug(
                f"Window isnt full, sending packet to host: {self.socket.host}\
                     and port: {self.socket.port} sending message \
                        with seq_num: {self.seq_num}")
            self.socket.send(message.as_bytes())
            self.messages_not_acked.append(message)
            sent = True

        # Process ACKS without blocking
        ack_bytes, _ = self.socket.read(const.MSG_SIZE, wait=False)
        if ack_bytes is not None:
            try:
                ack_segment = protocol.RDTPSegment.from_bytes(ack_bytes)
                self.remove_in_flight_messages(ack_segment)
            except struct.error as error:
                logging.error(f"Conversion error {error}")

        # If the window was full => block until there is room
        if not sent:
            if len(self.messages_not_acked) == self.window_size:
                self.await_ack()
            # reattempt to send after wait
            logging.debug(
                f"Window was full, sending packet to host: {self.socket.host}\
                     and port: {self.socket.port} sending message \
                        with seq_num: {self.seq_num}")
            attempts += 1
            self.send(data, attempts)

    def remove_in_flight_messages(self, ack_segment):
        """
        Process a packet. If it's an ACK, remove it and all previous ones
        from the message_not_acked list and return True.
        """

        self.finished = ack_segment.header.is_fin()
        for i in range(len(self.messages_not_acked)):
            if self.messages_not_acked[i].header.seq_num \
                    == ack_segment.header.ack_num:
                self.messages_not_acked = self.messages_not_acked[i + 1:]
                logging.debug(
                    f"Acked message {ack_segment.header.ack_num} \
                        and messages not acked {len(self.messages_not_acked)}")
                self.ack_num = ack_segment.header.ack_num
                return True
        return False

    def await_ack(self):
        """
        Waits and processes an ACK packet. If a timeout occurs without any new
        ACK from the in-flight list, resend the packets in the list.
        """
        try:
            ack_bytes, _ = self.socket.read(const.MSG_SIZE)
            if ack_bytes is not None:
                self.remove_in_flight_messages(
                    protocol.RDTPSegment.from_bytes(ack_bytes))
        except (socket.timeout, struct.error) as error:
            logging.debug(f"Timeout or conversion error {error}")
            if len(self.messages_not_acked) == 0:
                return
            # Re-send unacknowledged pkts
            logging.debug("Timeout without no new ack, resending packets")
            for message in self.messages_not_acked:
                self.socket.send(message.as_bytes())

    def close(self):
        attempts = 0
        while len(
                self.messages_not_acked) != 0 and\
                attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            attempts += 1
            self.await_ack()
        super().close()
