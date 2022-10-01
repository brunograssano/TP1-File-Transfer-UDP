import logging
import os
import shutil
import threading

from lib.InitialMessage import InitialMessage
from lib.file_manager import FileManager
from lib.rdtpstream import RDTPStream
from lib.protocols.stop_and_wait import StopAndWait
from lib.protocols.go_back_n import GoBackN

import lib.constants as constants
class UploadClientThread(threading.Thread):

    def __init__(self, server, initial_message : InitialMessage, client_socket : RDTPStream, storage : str):
        threading.Thread.__init__(self)
        self.file_size = initial_message.get_file_size()
        self.filename = initial_message.get_filename()
        self.storage = storage
        self.server = server
        self.socket = client_socket
        if initial_message.is_stop_and_wait():
            self.protocol = StopAndWait(client_socket)
        else:
            self.protocol = GoBackN()

    def run(self):
        if not os.path.isdir(self.storage):
            logging.info("Creating storage folder")
            os.makedirs(self.storage, exist_ok=True)

        total, used, free = shutil.disk_usage(self.storage)
        segment = self.protocol.listen_to_handshake(self.file_size < free)
        
        if free < self.file_size:
            self.protocol.close()
            self.server.remove_client(self.socket.gethost(), self.socket.getport())
            return

        file = FileManager(self.filename,"wb",0)
        read = 0
        while read < self.file_size:
            data = self.protocol.read(constants.MSG_SIZE)
            file.write(data)

        file.close()
        self.protocol.close()
        self.server.remove_client(self.socket.gethost(), self.socket.getport())