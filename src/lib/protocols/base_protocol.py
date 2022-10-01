import logging
from socket import timeout
import lib.constants as const
from socket import socket
from lib.InitialMessage import InitialMessage
from lib.rdtpstream import RDTPStream
from lib.segments.RDTPSegment import RDTPSegment
from lib.segments.headers.RDTPHeader import RDTPHeader

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
        header = RDTPHeader(0, 0, False) 
        segment = RDTPSegment(initial_msg.as_bytes(), header)

        attempts = 0
        self.socket.settimeout(const.CLIENT_HANDSHAKE_TIMEOUT)
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                self.socket.send(segment.as_bytes(), self.socket.host, self.socket.port)
                answer, address = self.socket.read(const.MSG_SIZE)
                self.socket.setaddress(address)

                segment = RDTPSegment.from_bytes(answer)
                return not segment.header.fin

            except timeout:
                attempts += 1
                continue 
        
        raise LostConnectionError("Lost connection error")


    def listen_to_handshake(self, is_space_available):
        header = RDTPHeader(0, 0, not is_space_available)
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

        raise LostConnectionError("Lost connection error")

    def close(self):
        logging.debug("Ending connection")
        header = RDTPHeader(self.seq_num, self.ack_num, True)
        segment = RDTPSegment(bytearray([]), header)
        self.socket.send(segment.as_bytes(), self.socket.gethost(), self.socket.getport())

        self.socket.close()

    def send(self, data):
        raise NotImplementedError()
    
    def read(self, buffer_size :int):
        raise NotImplementedError()





