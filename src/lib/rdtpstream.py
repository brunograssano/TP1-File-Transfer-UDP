from socket import *

class RDTPStream():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def bind(self):
        self.socket.bind((self.host, self.port))

    @staticmethod
    def server_socket(host, port):
        socket = RDTPStream(host,port)
        socket.bind()
        return socket

    @staticmethod
    def client_socket(host, port):
        return RDTPStream(host,port)

    def gethost(self):
        return self.socket.getsockname()[0]

    def getport(self):
        return self.socket.getsockname()[1]

    def read(self,buffersize):
        message, clientAddress = self.socket.recvfrom(buffersize)
        self.client = clientAddress
        return message

    def send(self,message):
        self.socket.sendto(message, self.socket.getpeername())

    def send(self,message, peer):
        self.socket.sendto(message, peer)
