from socket import timeout
import src.lib.constants as const
from socket import socket
from src.lib.InitialMessage import InitialMessage
from src.lib.rdtpstream import RDTPStream
from src.lib.segments.RDTPSegment import RDTPSegment
from src.lib.segments.headers.RDTPHeader import RDTPHeader

class LostConnectionError(Exception):
    pass

class BaseProtocol:
    def __init__(self, socket, is_stop_and_wait):
        self.socket: RDTPStream = socket
        self.is_stop_and_wait = is_stop_and_wait
        self.seq_num = 0
        self.ack_num = 0

    def send_handshake(self, file_size, file_name):
        initial_msg = InitialMessage.upload_message(file_size, file_name, self.is_stop_and_wait)
        header = RDTPHeader(0, 0, 10, False, False) 
        segment = RDTPSegment(initial_msg.as_bytes(), header)

        attempts = 0
        self.socket.settimeout(const.CLIENT_HANDSHAKE_TIMEOUT)
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                self.socket.send(segment.as_bytes(), self.socket.gethost(), self.socket.getport())
                answer, address = self.socket.read(const.MSG_SIZE)
                self.socket.setaddress(address)

                segment = RDTPSegment.from_bytes(answer)
                return not segment.header.fin

            except timeout:
                attempts += 1
                continue 
        
        return False

    def listen_to_handshake(self, is_space_available):
        header = RDTPHeader(0, 0, 10, True, not is_space_available)
        segment = RDTPSegment(bytearray([]), header)

        attempts = 0
        self.socket.settimeout(const.SERVER_HANDSHAKE_TIMEOUT)
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                self.socket.send(segment.as_bytes(), self.socket.gethost(), self.socket.getport())
                answer, _ = self.socket.read(const.MSG_SIZE)
                segment = RDTPSegment.from_bytes(answer)
                return segment

            except timeout:
                attempts += 1
                continue

    def close(self):
        header = RDTPHeader(self.seq_num, self.ack_num, 10, True, True)
        segment = RDTPSegment(bytearray([]), header)
        self.socket.send(segment.as_bytes(), self.socket.gethost(), self.socket.getport())





