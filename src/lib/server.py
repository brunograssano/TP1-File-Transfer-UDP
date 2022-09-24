import lib.constants as constants
from socket import *
import logging
from lib.DownloadClientThread import DownloadClientThread
from lib.RdtpListener import RDTPListener


from lib.UploadClientThread import UploadClientThread

class Server:

    def __init__(self,server_name: str, server_port: int):
        self.clients = []
        self.server_socket = RDTPListener(server_name,server_port)

    def start_server(self):
        logging.info("Ready to receive connections")
        while True:
            print("Antes del listen")
            initial_message, client_socket = self.server_socket.listen()
            print("Recibido")
            if initial_message.is_upload():
                thread = UploadClientThread(initial_message, client_socket)
            else:
                thread = DownloadClientThread(initial_message, client_socket)

            print("Se creo thread")
            self.clients.append(thread)
            thread.start()
            print("Empezo")

    def close(self):
        self.server_socket.close()
        # for client in clients:
        #     client.join()