import threading
from lib.InitialMessage import *
from lib.rdtpstream import *
from lib.protocols.stop_and_wait import StopAndWait
from lib.protocols.go_back_n import GoBackN

# Thread del lado del server que va a manejar la descarga
class DownloadClientThread(threading.Thread):

    def __init__(self, server, initial_message : InitialMessage, client_socket : RDTPStream, storage : str):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.filename = initial_message.get_filename()
        self.storage = storage
        self.server = server
        if initial_message.is_stop_and_wait():
            self.protocol = StopAndWait(client_socket, 1)
        else:
            self.protocol = GoBackN(1)
        # TODO crear el protocolo en base a initial_message.is_stop_and_wait()

        #al final de todo o antes de cualquier return:
        self.server.remove_client(self.client_socket.gethost(), self.client_socket.getport())

    def run(self):
        print("hola")

