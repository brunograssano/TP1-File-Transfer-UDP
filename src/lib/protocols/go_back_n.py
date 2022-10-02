import logging
import socket
import os
import struct
import time

import lib.constants as const
from lib.protocols.base_protocol import BaseProtocol
import lib.segments.RDTPSegment as protocol
import lib.segments.headers.RDTPHeader as rdtp_header
from lib.protocols.base_protocol import BaseProtocol, LostConnectionError

class GoBackN(BaseProtocol):
    def __init__(self, socket):
        super().__init__(socket, False)
        socket.setblocking(False)
        self.window_size = 10
        self.messages_not_acked = []

    def send(self, data):
        """
        Send data through the socket, creating the necessary headers.
        If an ACK is not received, the packet is added to the in-flight list.
        If the in-flight list is full, awaits ACKs for packages in the list.
        """
        #Create packet
        self.seq_num += 1
        head = rdtp_header.RDTPHeader(seq_num=self.seq_num, ack_num=self.ack_num, fin=False)
        message = protocol.RDTPSegment(data=data, header=head)
        sent = False


        #If the window isnt full, send packet
        if len(self.messages_not_acked) < self.window_size:
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
                logging.error(error)

        # If the window was full => block until there is room
        if not sent:
            if len(self.messages_not_acked) == self.window_size:
                self.await_ack()
            # reattempt to send after wait
            self.socket.send(message.as_bytes())
            self.messages_not_acked.append(message)


    def remove_in_flight_messages(self, ack_segment):
        """
        Process a packet. If it's an ACK, remove it and all previous ones
        from the message_not_acked list and return True.
        """
        for i in range(len(self.messages_not_acked)):
            if self.messages_not_acked[i].header.seq_num == ack_segment.header.ack_num:
                self.messages_not_acked = self.messages_not_acked[i + 1 :]
                return True
        return False


    def await_ack(self):
        """
        Waits and processes an ACK packet. If a timeout occurs without any new
        ACK from the in-flight list, resend the packets in the list.
        """
        attempts = 0
        try:
            ack_bytes, _ = self.socket.read(const.MSG_SIZE)
            if ack_bytes is not None and self.remove_in_flight_messages(protocol.RDTPSegment.from_bytes(ack_bytes)):
                self.tries = 0
        except (socket.timeout, struct.error) as error:
            logging.error(error)
            if not self.messages_not_acked:
                return
            # Re-send unacknowledged pkts
            attempts += 1
            for message in self.messages_not_acked:
                self.socket.send(message.as_bytes())

    def read(self, buffer_size :int):
        self.seq_num += 1
        attempts = 0
        is_new_data = False
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                segment_bytes, _ = self.socket.read(buffer_size)
                segment = protocol.RDTPSegment.from_bytes(segment_bytes)
            except (socket.timeout, struct.error) as error:
                logging.error(error)
                attempts += 1
                continue


            if segment.header.seq_num == (self.ack_num + 1):
                self.ack_num = segment.header.seq_num
                is_new_data = True

            head = rdtp_header.RDTPHeader(seq_num=self.seq_num, ack_num=self.ack_num, fin=False)
            ack_message = protocol.RDTPSegment(data=bytearray([]), header=head)
            self.socket.send(ack_message.as_bytes())
            if is_new_data:
                return segment.data

        raise LostConnectionError("Lost connection error")

    def close(self):
        while len(self.messages_not_acked) != 0:
            self.await_ack()
        super().close()
