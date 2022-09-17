from socket import *
from rdtpstream import RDTPStream


class RDTPListener():
    def __init__(self, host, port):
        self.welcoming_socket = socket(AF_INET, SOCK_DGRAM)
        self.welcoming_socket.bind((host, port))

    def listen(self):
        message, clientAddress = self.welcoming_socket.recvfrom(2048)
        client_socket = RDTPStream('', 0)
        host = client_socket.gethost()
        port = client_socket.getport()
        self.welcoming_socket.sendto((str(host) + ":" + str(port)).encode, clientAddress)
        return client_socket
