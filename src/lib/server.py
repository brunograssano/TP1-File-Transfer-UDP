import logging
from lib.DownloadClientThread import DownloadClientThread
from lib.rdtplistener import RDTPListener
from threading import Lock


from lib.UploadClientThread import UploadClientThread


class Server:

    def __init__(self, server_name: str, server_port: int, storage: str):
        self.clients = {}
        self.client_threads = []
        self.client_mutex = Lock()
        self.storage = storage
        self.server_socket = RDTPListener(server_name, server_port)

    def start_server(self):
        logging.info("Ready to receive connections")
        while True:
            initial_message, client_socket, client_address =\
                 self.server_socket.listen()
            self.add_client(initial_message, client_address, client_socket)

    def add_client(self, initial_message, client_address, client_socket):
        self.client_mutex.acquire()
        if (client_address[0], client_address[1]) not in self.clients:
            logging.info("Received a new client request")
            if initial_message.is_upload():
                thread = UploadClientThread(
                    self,
                    initial_message,
                    client_address,
                    self.storage,
                    client_socket)
            else:
                thread = DownloadClientThread(
                    self, initial_message, client_address, self.storage,
                    client_socket)

            self.clients[(client_address[0], client_address[1])] = True
            self.client_threads.append(thread)
            thread.start()
            logging.debug("Started thread for a new client")
        self.client_mutex.release()

    def remove_client(self, host, port):
        self.client_mutex.acquire()
        self.clients.pop((host, port))
        self.client_mutex.release()

    def close(self):
        self.server_socket.close()
        for client in self.client_threads:
            client.close()
            client.join()
