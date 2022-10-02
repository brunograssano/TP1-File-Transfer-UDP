from cmath import e
import logging
from socket import timeout
import struct
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

    def send_handshake(self, file_size, file_name, is_upload):
        if(is_upload):
            initial_msg = InitialMessage.upload_message(file_size, file_name, self.is_stop_and_wait)
        else:
            initial_msg = InitialMessage.download_message(file_name, self.is_stop_and_wait)

        header = RDTPHeader(0, 0, False) 
        segment = RDTPSegment(initial_msg.as_bytes(), header)

        attempts = 0
        self.socket.settimeout(const.CLIENT_HANDSHAKE_TIMEOUT)
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending first message of handshake")
                self.socket.send(segment.as_bytes())
                answer, address = self.socket.read(const.MSG_SIZE)
                logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} received second message of handshake")
                self.socket.setaddress(address)
                response_segment = RDTPSegment.from_bytes(answer)
                initial_msg_response = InitialMessage.from_bytes(response_segment.data)

                third_handshake_step_header = RDTPHeader(0, 0, response_segment.header.fin)
                third_handshake_step_segment = RDTPSegment(bytearray([]), third_handshake_step_header)
                logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending third message of handshake")
                self.socket.send(third_handshake_step_segment.as_bytes())

                return not response_segment.header.fin, initial_msg_response.file_size

            except (timeout, struct.error) as error:
                logging.error(f"Timeout or conversion error {error}")
                attempts += 1
                continue 
        
        raise LostConnectionError("Lost connection error")


    def listen_to_handshake(self, is_space_available, file_size, file_name, is_upload):

        if(is_upload):
            initial_msg = InitialMessage.upload_message(file_size, file_name, self.is_stop_and_wait)
        else:
            initial_msg = InitialMessage.download_message(file_name, self.is_stop_and_wait)
            initial_msg.file_size = file_size

        header = RDTPHeader(0, 0, not is_space_available)
        segment = RDTPSegment(initial_msg.as_bytes(), header)

        attempts = 0
        self.socket.settimeout(const.SERVER_HANDSHAKE_TIMEOUT)
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending second message of handshake")
                self.socket.send(segment.as_bytes())
                answer, _ = self.socket.read(const.MSG_SIZE)
                logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending third message of handshake")
                segment = RDTPSegment.from_bytes(answer)
                return segment

            except (timeout, struct.error) as error:
                logging.error(f"Timeout or conversion error {error}")
                attempts += 1
                continue

        raise LostConnectionError("Lost connection error")

    def close(self):
        logging.debug("Ending connection")
        header = RDTPHeader(self.seq_num, self.ack_num, True)
        segment = RDTPSegment(bytearray([]), header)
        logging.debug(f"Socket in host: {self.socket.host} and port: {self.socket.port} sending message to end connection")
        self.socket.send(segment.as_bytes())

        self.socket.close()

    def send(self, data):
        raise NotImplementedError()
    
    def read(self, buffer_size :int):
        raise NotImplementedError()





