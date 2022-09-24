import socket
import os
import time

import utils as utils
import constants as constants

WAITING_TIME = 60

class StopAndWaitClient:
    def __init__(self, verbose=1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.last_packet_time = time.time()
        self.verbosity = verbose

    def is_dead(self):
        return ((time.time() - self.last_packet_time) > WAITING_TIME)

    def upload_file(self, storage_path, file_name, name, port):
        file_path = f"{storage_path}/{file_name}"

        if not os.path.isfile(file_path):
            utils.print_file_not_found_error(file_path)
            return 1

        file_size = os.path.getsize(file_path)
        #todo Handshake
        self.handshake(file_name, file_size, name, port)

        if self.verbosity >= 1:
            print(f"{constants.COLOR_BLUE}[INFO]{constants.COLOR_END}"
                  f" - Ready to upload to {name} on port {port}")
        #todo seguir


    def download_file(self, storage_path, file_name, name, port):
        file_path = f"{storage_path}/{file_name}"
        #todo Handshake
        file_size = self.handshake(file_name, 0, name, port)

        if self.verbosity >= 1:
            print(f"{constants.COLOR_BLUE}[INFO]{constants.COLOR_END}"
                  f" - Ready to download from {name} on port {port}")

        if file_size == 0:
            utils.print_file_not_exists(file_name)
            return 1
        else:
            utils.print_file_exists(file_name, self.verbosity)
        #todo seguir

    #todo ver que necesita el handshake
    def handshake(self, file_name, file_size, name, port):
        ...

    def __del__(self):
        self.socket.close()