import logging
import os
import shutil
import threading

from lib.InitialMessage import InitialMessage
from lib.file_manager import FileManager
from lib.rdtpstream import RDTPStream

import constants
class UploadClientThread(threading.Thread):

    def __init__(self, initial_message : InitialMessage, client_socket : RDTPStream, storage : str):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.file_size = initial_message.get_file_size()
        self.filename = initial_message.get_filename()
        self.storage = storage
        # TODO crear el protocolo en base a initial_message.is_stop_and_wait()

    def run(self):
        if not os.path.isdir(self.storage):
            logging.info("Creating storage folder")
            os.makedirs(self.storage, exist_ok=True)

        total, used, free = shutil.disk_usage(self.storage)
        self.client_socket.can_save_file(self.file_size < free)
        if free < self.file_size:
            self.client_socket.close()
            return

        file = FileManager(self.filename,"wb",0)
        read = 0
        while read < self.file_size:
            data = self.client_socket.read(constants.MSG_SIZE)
            file.write(data)

        file.close()
        self.client_socket.close()