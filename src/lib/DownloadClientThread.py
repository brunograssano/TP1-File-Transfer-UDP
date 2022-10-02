import lib.constants as constants
import logging
import os
import shutil
import threading
from lib.InitialMessage import *
from lib.rdtpstream import *
from lib.file_manager import FileManager
from lib.protocols.base_protocol import LostConnectionError
from lib.protocols.go_back_n import GoBackN
from lib.protocols.stop_and_wait import StopAndWait
from lib.file_manager import FileManagerError

# Thread del lado del server que va a manejar la descarga
class DownloadClientThread(threading.Thread):

    def __init__(self, server, initial_message : InitialMessage, client_address, storage : str,  client_socket : RDTPStream):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.filename = initial_message.get_filename()
        self.storage = storage
        self.server = server
        self.client_address = client_address
        if initial_message.is_stop_and_wait():
            self.protocol = StopAndWait(client_socket)
        else:
            self.protocol = GoBackN(client_socket)

    def run(self):
        file_path = os.path.join(self.storage, self.filename)
        if not os.path.isfile(file_path):
            logging.error(f"File in {file_path} doesn't exists")
            segment = self.protocol.listen_to_handshake(False, 0, self.filename, False)
            return

        file_size = os.path.getsize(file_path)
        file = None
        logging.debug(f"Sending file {self.filename} of {file_size} to client")
        try:
            segment = self.protocol.listen_to_handshake(True, file_size, self.filename, False)
            if segment.header.fin:
                return

            file = FileManager(self.filename,"rb")

            while file_size > 0:
                read_size = min(file_size, constants.MSG_SIZE)
                data = file.read(read_size)
                self.protocol.send(data)
                file_size = file_size - read_size

        except FileManagerError:
            logging.error("Error with file manager, finishing connection")
        except LostConnectionError:            
            logging.error("Lost connection to client. ")
        finally:
            if file is not None:
                file.close()
            self.protocol.close()
        
        self.server.remove_client(self.client_address[0], self.client_address[1])
            

