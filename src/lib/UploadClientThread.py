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

    def __init__(self, initial_message : InitialMessage, client_socket : RDTPStream, storage : str):
        threading.Thread.__init__(self)
        self.file_size = initial_message.get_file_size()
        self.filename = initial_message.get_filename()
        self.storage = storage
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
            return
        file_path = os.path.join(self.storage,self.filename)
        new_file_path = file_path.split('\x00')[0]
        file = FileManager(new_file_path,"wb",0)
        # todo solucionar como actualizar el puntero write
        write = 0
        print("tamanio de archivo: ", self.file_size)
        while write < self.file_size:
            print("puntero: ", write)
            data = self.protocol.read(constants.MSG_SIZE)
            file.write(data)
            # actualizar puntero
            write += constants.MSG_SIZE

        file.close()
        self.protocol.close()