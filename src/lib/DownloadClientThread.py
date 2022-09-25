import threading
from lib.InitialMessage import *
from lib.rdtpstream import *

# Thread del lado del server que va a manejar la descarga
class DownloadClientThread(threading.Thread):

    def __init__(self, initial_message : InitialMessage, client_socket : RDTPStream, storage : str):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.filename = initial_message.get_filename()
        self.storage = storage

    def run(self):
        print("hola")

