import socket
import os
import time

import lib.utils as utils
import lib.constants as constants
from src.lib.protocols.base_protocol import BaseProtocol

class GoBackN(BaseProtocol):
    def __init__(self, verbose=1):
        super.__init__(socket, False)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.last_packet_time = time.time()
        self.verbosity = verbose