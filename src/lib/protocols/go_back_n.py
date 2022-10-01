import socket
import os
import time

import lib.constants as constants
from lib.protocols.base_protocol import BaseProtocol

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
        while ack_bytes is not None:
            ack_segment = protocol.RDTPSegment.from_bytes(ack_bytes)
            self.remove_in_flight_messages(ack_segment)

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
        try:
            ack_bytes, _ = self.socket.read(const.MSG_SIZE)
            if ack_bytes is not None and self.remove_in_flight_messages(protocol.RDTPSegment.from_bytes(ack_bytes)):
                self.tries = 0
        except socket.timeout:
            if not self.messages_not_acked:
                return
            # Re-send unacknowledged pkts
            self.tries += 1
            for message in self.messages_not_acked:
                self.socket.send(message.as_bytes())

    def read(self, buffer_size :int):
