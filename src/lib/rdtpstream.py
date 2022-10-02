import logging
import select
import socket

import lib.constants as const

from lib.segments.headers.RDTPHeader import RDTPHeader

class RDTPStream():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

    def setblocking(self, flag):
        self.socket.setblocking(flag)

    def read(self,buffersize :int, wait=True):
        message, clientAddress = (None, None)
        ready = select.select([self.socket], [], [], const.CLIENT_STOP_AND_WAIT_TIMEOUT if wait else 0)
        if ready[0]:
            message, clientAddress = self.socket.recvfrom(buffersize + RDTPHeader.size())
        elif wait:
            raise socket.timeout

        return message, clientAddress

    def send(self, message):
        self.socket.sendto(message, (self.host, self.port))

    def close(self):
        logging.debug("Closing socket")
        self.socket.close()
