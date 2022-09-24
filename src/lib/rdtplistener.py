from socket import *
from lib.InitialMessage import InitialMessage
from lib.rdtpstream import RDTPStream
import logging

class RDTPListener():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.welcoming_socket = socket(AF_INET, SOCK_DGRAM)
        self.welcoming_socket.bind((host, port))

    def listen(self):
        message, client_address = self.welcoming_socket.recvfrom(2048)
        logging.info("Received a new client request")
        client_socket = RDTPStream.server_client_socket(client_address[0],client_address[1])
        return InitialMessage.from_bytes(message), client_socket

    def close(self):
        self.welcoming_socket.close()
