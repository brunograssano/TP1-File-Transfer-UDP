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
from lib.protocols.base_protocol import LostConnectionError
from lib.file_manager import FileManagerError


class UploadClientThread(threading.Thread):

    def __init__(
            self,
            server,
            initial_message: InitialMessage,
            client_address,
            storage: str,
            client_socket: RDTPStream):
        threading.Thread.__init__(self)
        self.file_size = initial_message.get_file_size()
        self.filename = initial_message.get_filename()
        self.storage = storage
        self.client_address = client_address
        self.filepath = os.path.join(self.storage, self.filename)
        self.server = server
        self.socket = client_socket
        self.running = True
        self.close_lock = threading.Lock()
        if initial_message.is_stop_and_wait():
            self.protocol = StopAndWait(client_socket)
        else:
            self.protocol = GoBackN(client_socket)

    def close(self):
        self.close_lock.acquire()
        if self.running:
            self.protocol.close()
            self.running = False
        self.close_lock.release()

    def run(self):
        if not os.path.isdir(self.storage):
            logging.info("Creating storage folder")
            os.makedirs(self.storage, exist_ok=True)

        total, used, free = shutil.disk_usage(self.storage)

        file = None
        try:
            segment = self.protocol.listen_to_handshake(
                self.file_size < free, self.file_size, self.filename, True)
            if free < self.file_size:
                logging.error("There is not enough space for file in disk")
                return

            logging.debug(
                f"Receiving file {self.filename} of {self.file_size} from client")
            file = FileManager(self.filepath, "wb")

            write = 0
            while not self.protocol.is_finished():
                data = self.protocol.read(constants.MSG_SIZE)
                if write < self.file_size and data is not None:
                    file.write(data)
                    write += constants.MSG_SIZE

            logging.info("End of client upload of file")
        except FileManagerError:
            logging.error("Error with file manager, finishing connection")
        except LostConnectionError:
            logging.error("Lost connection to client. ")
            if file is not None:
                file.close()
                os.remove(self.filepath)
        except Exception as e:
            logging.error("Closing error. {}".format(e))
        finally:
            self.close_lock.acquire()
            if self.running:
                self.protocol.close()
                self.running = False
            self.close_lock.release()
            self.server.remove_client(
                self.client_address[0],
                self.client_address[1])
