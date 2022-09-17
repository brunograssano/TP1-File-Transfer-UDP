from socket import *

class RDTPStream():
    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))

    def gethost():
        return self.socket.getsockname()[0]

    def getport():
        return self.socket.getsockname()[1]

    def read(buffersize):
        message, clientAddress = client_socket.recvfrom(buffersize)
        self.client = clientAddress
        return message

    def send(message):
        self.socket.sendto(message.encode(), self.socket.getpeername())
