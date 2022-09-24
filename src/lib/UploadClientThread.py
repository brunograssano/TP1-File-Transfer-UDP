import threading

from lib.InitialMessage import InitialMessage
from lib.RdtpStream import RDTPStream

class UploadClientThread(threading.Thread):

    def __init__(self, initial_message : InitialMessage, client_socket : RDTPStream):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.file_size = initial_message.get_file_size()

    def run(self):
        self.client_socket.send("holas".encode())
        print("hola")