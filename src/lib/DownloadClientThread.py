from asyncio import constants
from lib.utils import print_file_not_found_error as utils
import logging
import os
import shutil
import threading
from lib.InitialMessage import *
from lib.rdtpstream import *
from src.lib.file_manager import FileManager
from src.lib.protocols.go_back_n import GoBackN
from src.lib.protocols.stop_and_wait import StopAndWait

# Thread del lado del server que va a manejar la descarga
class DownloadClientThread(threading.Thread):

    def __init__(self, initial_message : InitialMessage, client_socket : RDTPStream, storage : str):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.file_size = initial_message.get_file_size()
        self.filename = initial_message.get_filename()
        self.storage = storage
        if initial_message.is_stop_and_wait():
            self.protocol = StopAndWait(client_socket)
        else:
            self.protocol = GoBackN()

    def run(self):
        file_path = os.path.join(self.storage, self.filename)
        if not os.path.isfile(file_path):
            utils.print_file_not_found_error(file_path)
            return

        file = FileManager(self.filename,"rb",0)

        while file_size > 0:
            read_size = min(file_size, constants.MSG_SIZE)
            data = file.read(read_size)
            self.protocol.send(data)
            file_size = file_size - read_size

        file.close()
        self.client_socket.close()

