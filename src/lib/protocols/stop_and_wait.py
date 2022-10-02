import logging
from socket import timeout
import struct


import lib.segments.RDTPSegment as protocol
import lib.segments.headers.RDTPHeader as rdtp_header
from lib.protocols.base_protocol import BaseProtocol, LostConnectionError
import lib.constants as const

class StopAndWait(BaseProtocol):
    def __init__(self, socket):
        super().__init__(socket, True)
        self.socket.settimeout(const.CLIENT_STOP_AND_WAIT_TIMEOUT)

    def send(self, data):
        self.seq_num += 1
        head = rdtp_header.RDTPHeader(seq_num=self.seq_num, ack_num=self.ack_num, fin=False)
        message = protocol.RDTPSegment(data=data, header=head)
        attempts = 0
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending message with seq_num: {self.seq_num}")
                self.socket.send(message.as_bytes())
                ack_bytes, _ = self.socket.read(const.MSG_SIZE)
                ack_segment = protocol.RDTPSegment.from_bytes(ack_bytes)
                if ack_segment.header.ack_num != self.seq_num:
                    continue
                self.ack_num = ack_segment.header.ack_num
                return

            except (timeout, struct.error) as error:
                logging.error(error)
                attempts += 1
                continue

        raise LostConnectionError("Lost connection error")


    def read(self, buffer_size :int):
        self.seq_num += 1
        attempts = 0
        is_new_data = False
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                segment_bytes, _ = self.socket.read(buffer_size)
                segment = protocol.RDTPSegment.from_bytes(segment_bytes)
            except (timeout, struct.error) as error:
                logging.error(error)
                attempts += 1
                continue

            if segment.header.seq_num == (self.ack_num + 1):
                self.ack_num = segment.header.seq_num
                is_new_data = True

            head = rdtp_header.RDTPHeader(seq_num=self.seq_num, ack_num=self.ack_num, fin=False)
            ack_message = protocol.RDTPSegment(data=bytearray([]), header=head)
            logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending message with ack: {self.ack_num}")
            self.socket.send(ack_message.as_bytes())
            if is_new_data:
                return segment.data

        raise LostConnectionError("Lost connection error")
