from socket import *

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

    def gethost(self):
        return self.socket.getsockname()[0]

    def getport(self):
        return self.socket.getsockname()[1]

    def read(self,buffersize):
        message, clientAddress = self.socket.recvfrom(buffersize)
        self.client = clientAddress
        return message

    def send(self, message, ip, port):
        self.socket.sendto(message, (ip, port))

    def close(self):
        self.socket.close()
