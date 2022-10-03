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
        head = rdtp_header.RDTPHeader(
            seq_num=self.seq_num,
            ack_num=self.ack_num,
            fin=False)
        message = protocol.RDTPSegment(data=data, header=head)
        attempts = 0
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                logging.debug(
                    f"Socket in host: {self.socket.host} and port: {self.socket.port} sending message with seq_num: {self.seq_num}")
                self.socket.send(message.as_bytes())
                ack_bytes, _ = self.socket.read(const.MSG_SIZE)
                ack_segment = protocol.RDTPSegment.from_bytes(ack_bytes)
                if ack_segment.header.ack_num != self.seq_num:
                    continue
                self.finished = ack_segment.header.is_fin()
                self.ack_num = ack_segment.header.ack_num
                return

            except (timeout, struct.error) as error:
                logging.debug(f"Timeout or conversion error {error}")
                attempts += 1
                continue

        self.finished = True
        raise LostConnectionError("Lost connection error")

