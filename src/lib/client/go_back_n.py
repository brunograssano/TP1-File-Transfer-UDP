import socket
import os
import time

import utils as utils
import constants as constants

class GoBackNClient:
    def __init__(self, verbose=1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.last_packet_time = time.time()
        self.verbosity = verbose