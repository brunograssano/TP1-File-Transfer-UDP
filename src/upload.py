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

def upload(server_name: str, server_port: int, src:str, file_name: str):

    file_path = os.path.join(src,file_name)
    if not os.path.isfile(file_path):
        utils.print_file_not_found_error(file_path)
        return

    file_size = os.path.getsize(file_path)

    client_socket = RDTPStream.client_socket(server_name,server_port)

    is_fin = client_socket.can_send_file(file_size, file_name)
    if is_fin:
        logging.error("Server does not have enough free disk")
        return

    file = FileManager(file_path, "rb")
    while file_size > 0:
        read_size = min(file_size, constants.MSG_SIZE)
        data = file.read(read_size)
        client_socket.send(data)
        file_size = file_size - read_size

    file.close()
    client_socket.close()


if __name__ == '__main__':
    args = upload_parser()
    upload(args.host[0],args.port[0],args.src[0],args.name[0])