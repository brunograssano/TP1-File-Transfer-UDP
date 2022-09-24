from socket import *

class RDTPStream():
    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))

    def gethost(self):
        return self.socket.getsockname()[0]

    def getport(self):
        return self.socket.getsockname()[1]

    def read(self,buffersize):
        message, clientAddress = self.socket.recvfrom(buffersize)
        self.client = clientAddress
        return message

    def send(self,message):
        self.socket.sendto(message.encode(), self.socket.getpeername())
