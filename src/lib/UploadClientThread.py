import shutil
import threading

from lib.InitialMessage import InitialMessage
from lib.file_manager import FileManager
from lib.rdtpstream import RDTPStream

import constants
class UploadClientThread(threading.Thread):

    def __init__(self, initial_message : InitialMessage, client_socket : RDTPStream):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.file_size = initial_message.get_file_size()
        self.filename = initial_message.get_filename()

    def run(self):
        total, used, free = shutil.disk_usage(".")
        if free < self.file_size:
            self.client_socket.close()
            return
        
        self.client_socket.accept()

        file = FileManager(self.filename,"wb",0)
        read = 0
        while read < self.file_size:
            data = self.client_socket.read(constants.MSG_SIZE)
            file.write(data)

        file.close()
        self.client_socket.close()