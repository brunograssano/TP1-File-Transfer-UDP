import logging
from socket import *
from lib.DownloadClientThread import DownloadClientThread
from lib.rdtplistener import RDTPListener


from lib.UploadClientThread import UploadClientThread

class Server:

    def __init__(self,server_name: str, server_port: int, storage : str):
        self.clients = []
        self.storage = storage
        self.server_socket = RDTPListener(server_name,server_port)

    def start_server(self):
        logging.info("Ready to receive connections")
        while True:
            initial_message, client_socket = self.server_socket.listen()
            logging.info("Received connection")
            if initial_message.is_upload():
                thread = UploadClientThread(initial_message, client_socket, self.storage)
            else:
                thread = DownloadClientThread(initial_message, client_socket, self.storage)

            self.clients.append(thread)
            thread.start()
            logging.debug("Started thread for a new client")

    def close(self):
        self.server_socket.close()
        # for client in clients:
        #     client.join()