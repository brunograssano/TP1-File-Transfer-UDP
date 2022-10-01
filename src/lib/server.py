from http import client
import logging
from socket import *
from lib.DownloadClientThread import DownloadClientThread
from lib.rdtplistener import RDTPListener
from threading import Thread, Lock


from lib.UploadClientThread import UploadClientThread

class Server:

    def __init__(self,server_name: str, server_port: int, storage : str):
        self.clients = {}
        self.client_threads = [] 
        self.client_mutex = Lock()
        self.storage = storage
        self.server_socket = RDTPListener(server_name,server_port)

    def start_server(self):
        logging.info("Ready to receive connections")
        while True:
            initial_message, client_socket = self.server_socket.listen()
            logging.info("Received connection")
            self.add_client(initial_message, client_socket) 

    def add_client(self, initial_message, client_socket):
        self.client_mutex.acquire()
        if (client_socket.gethost(), client_socket.getport()) not in self.clients:
            if initial_message.is_upload():
                thread = UploadClientThread(self, initial_message, client_socket, self.storage)
            else:
                thread = DownloadClientThread(self, initial_message, client_socket, self.storage)
           
            self.clients[(client_socket.gethost(), client_socket.getport())] = True
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
            client.join()