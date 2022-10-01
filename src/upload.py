from asyncio import constants
import logging
import os
from socket import *

from lib.file_manager import FileManager
from lib.rdtpstream import RDTPStream
from lib.parser import upload_parser
from lib.protocols.go_back_n import GoBackN
from lib.protocols.stop_and_wait import StopAndWait
from lib.log import set_up_logger
from lib.protocols.base_protocol import LostConnectionError
import lib.constants as constants

def upload(server_name: str, server_port: int, src:str, file_name: str, is_saw : bool):

    file_path = os.path.join(src,file_name)
    if not os.path.isfile(file_path):
        logging.error(f"File in {file_path} does not exists")
        return

    file_size = os.path.getsize(file_path)
    logging.debug(f"Found file in {file_path} with size {file_size} bytes")

    client_socket = RDTPStream.client_socket(server_name,server_port)
    
    if is_saw:
        protocol = StopAndWait(client_socket)
    else: 
        protocol = GoBackN()

    file = None
    try:
        can_send = protocol.send_handshake(file_size, file_name, True)
        if not can_send:
            protocol.close()
            logging.error("Server does not have enough free disk")
            return

        file = FileManager(file_path, "rb")
        while file_size > 0:
            read_size = min(file_size, constants.MSG_SIZE)
            data = file.read(read_size)
            protocol.send(data)
            file_size = file_size - read_size

    except LostConnectionError:
        logging.error("Lost connection to server. ")
    finally:
        if file is not None:
            file.close()
        protocol.close()

if __name__ == '__main__':
    args = upload_parser()
    set_up_logger(args, constants.UPLOAD_LOG_FILENAME)
    logging.info("Starting client")
    upload(args.host[0],args.port[0],args.src[0],args.name[0],args.stop_and_wait)
    logging.info("End of execution")