import logging
from socket import *

from lib.segments.headers.RDTPHeader import RDTPHeader

class RDTPStream():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def bind(self, peer):
        self.socket.bind(peer)

    @staticmethod
    def server_welcoming_socket(host, port):
        socket = RDTPStream(host,port)
        socket.bind(("",port))
        return socket

    @staticmethod
    def server_client_socket(host, port):
        socket = RDTPStream(host,port)
        socket.bind(("",0))
        return socket

    @staticmethod
    def client_socket(host, port):
        return RDTPStream(host,port)

    def settimeout(self, seconds):
        self.socket.settimeout(seconds)

    def setaddress(self, address):
        self.host = address[0]
        self.port = address[1]

    def gethost(self):
        return self.socket.getsockname()[0]

    def getport(self):
        return self.socket.getsockname()[1]

    def read(self,buffersize :int):
        message, clientAddress = self.socket.recvfrom(buffersize + RDTPHeader.size())
        return message, clientAddress

    def send(self, message):
        self.socket.sendto(message, (self.host, self.port))

    def close(self):
        logging.debug("Closing socket")
        self.socket.close()
