from asyncio import constants
import logging
import os
from socket import *
from lib.InitialMessage import InitialMessage
from lib.file_manager import FileManager
from lib.rdtpstream import RDTPStream
from lib.parser import upload_parser
from lib.segments.RDTPSegment import RDTPSegment
from lib.utils import print_file_not_found_error as utils
import lib.constants as constants
from lib.protocols.go_back_n import GoBackN
from lib.protocols.stop_and_wait import StopAndWait

def upload(server_name: str, server_port: int, src:str, file_name: str, is_saw : bool):

    file_path = os.path.join(src,file_name)
    if not os.path.isfile(file_path):
        utils.print_file_not_found_error(file_path)
        return

    file_size = os.path.getsize(file_path)


    # TODO Crear el protocolo en base a is_saw (stop and wait) que va a tener al socket
    client_socket = RDTPStream.client_socket(server_name,server_port)
    
    if is_saw:
        protocol = StopAndWait(client_socket, 1)
    else: 
        protocol = GoBackN(1)

    can_send = protocol.send_handshake(file_size, file_name)
    if not can_send:
        protocol.close()
        logging.error("Server does not have enough free disk or is unreachable")
        return

    file = FileManager(file_path, "rb")
    while file_size > 0:
        read_size = min(file_size, constants.MSG_SIZE)
        data = file.read(read_size)
        protocol.send(data, server_name, server_port)
        file_size = file_size - read_size

    file.close()
    protocol.close()


if __name__ == '__main__':
    args = upload_parser()
    upload(args.host[0],args.port[0],args.src[0],args.name[0],args.stop_and_wait)