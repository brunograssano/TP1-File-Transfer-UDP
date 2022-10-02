from socket import *
from lib.InitialMessage import InitialMessage
from lib.rdtpstream import RDTPStream
import logging

from lib.segments.RDTPSegment import RDTPSegment

class RDTPListener():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.welcoming_socket = RDTPStream.server_welcoming_socket(host, port)

    def listen(self):
        while True:
            try:
                message, client_address = self.welcoming_socket.read(2048)
            except timeout:
                continue
            segment = RDTPSegment.from_bytes(message)
            logging.debug("Client request coming from: " + str(client_address))
            client_socket = RDTPStream.server_client_socket(client_address[0],client_address[1])
            return InitialMessage.from_bytes(segment.data), client_socket, client_address

    def close(self):
        self.welcoming_socket.close()
