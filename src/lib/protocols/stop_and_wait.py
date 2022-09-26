import socket
import os
import time

from socket import timeout

import lib.utils as utils
import lib.constants as constants

import lib.InitialMessage as init_msn
import lib.segments.RDTPSegment as protocol
import lib.segments.headers.RDTPHeader as rdtp_header
from src.lib.protocols.base_protocol import BaseProtocol, LostConnectionError
import src.lib.constants as const

class StopAndWait(BaseProtocol):
    def __init__(self, socket, verbose=1):
        super.__init__(socket=socket, is_stop_and_wait=True)
        self.verbosity = verbose
        self.socket.settimeout(const.CLIENT_STOP_AND_WAIT_TIMEOUT)

    def send(self, data):
        self.seq_num += 1
        head = rdtp_header.RDTPHeader(seq_num=self.seq_num, ack_num= self.ack_num, window=0, ack_only=False, fin=False)
        message = protocol.RDTPSegment(data=data, header=head)
        attempts = 0
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                self.socket.send(message.as_bytes())
                # message, clientAddress
                ack_bytes, _ = self.socket.read(const.MSG_SIZE)
                ack_segment = protocol.RDTPSegment.from_bytes(ack_bytes)
                # ? Message responded by ACK number
                if ack_segment.header.ack_num != self.seq_num:
                    # ? I recieved an old or duplicated ACK
                    continue
                self.ack_num = ack_segment.header.ack_num
                return

            except timeout:
                attempts += 1
                continue
        # * Creo y devuelvo una excepcion que no se pudo mandar
        raise LostConnectionError("Lost connection error")

    # ? Espero recibir datos y envio ACKs
    def read(self, buffer_size) -> bytearray:
        self.seq_num += 1
        attempts = 0
        is_new_data = False
        while attempts < const.TIMEOUT_RETRY_ATTEMPTS:
            try:
                # message, clientAddress
                segment_bytes, _ = self.socket.read(buffer_size)
                segment = protocol.RDTPSegment.from_bytes(segment_bytes)

                #! ack del seq num que recibimos si, recibimos seq num = 3
                #! hacemos ack de 3.
                #! Si recibimos seq num = 2, pero teniamos ack = 3, devolvemos ack = 3
                if segment.header.seq_num == (self.ack_num + 1):
                    #? esta todo OK
                    self.ack_num = segment.header.seq_num
                    is_new_data = True
                #! si no actualizamos el ack num, es porque el paquete se perdio, y hay que volver a hacer ack de lo viejo
                head = rdtp_header.RDTPHeader(seq_num=self.seq_num, ack_num= self.ack_num, window=0, ack_only=True, fin=False)
                ack_message = protocol.RDTPSegment(data=bytearray([]), header=head)
                self.socket.send(ack_message.as_bytes())
                if is_new_data:
                    return segment.data

            except timeout:
                attempts += 1
                continue
        raise LostConnectionError("Lost connection error")
