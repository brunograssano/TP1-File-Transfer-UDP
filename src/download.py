import os
import sys
import logging
import lib.constants as constants
from lib.parser import download_parser
from lib.protocols.stop_and_wait import StopAndWait
from lib.protocols.go_back_n import GoBackN
from lib.file_manager import FileManager
from lib.log import set_up_logger
from lib.protocols.base_protocol import LostConnectionError
from lib.rdtpstream import RDTPStream

def download(server_name: str, server_port: int, dst:str, file_name: str, is_saw : bool):

    if not os.path.isdir(dst):
        os.makedirs(dst, exist_ok=True)

    client_socket = RDTPStream.client_socket(server_name,server_port)
    
    if is_saw:
        protocol = StopAndWait(client_socket)
    else: 
        protocol = GoBackN()
    file = None
    try:
        can_download = protocol.send_handshake(0, file_name, False)
        if not can_download:
            protocol.close()
            logging.error("File not found in server")
            return

        file_path = os.path.join(dst,file_name)

        file = FileManager(file_path, "wb")
        while file_size > 0:        
            read_size = min(file_size, constants.MSG_SIZE)
            data = protocol.read(read_size)
            file.write(data)
            file_size = file_size - read_size

        file.close()

    except LostConnectionError:
        if file is not None:
            file.close()
            file_path = os.path.join(dst,file_name)
            os.remove(file_path)
        logging.error("Lost connection error")

    finally:
        protocol.close()


if __name__ == '__main__':
    args = download_parser()
    set_up_logger(args, constants.DOWNLOAD_LOG_FILENAME)
    logging.info("Starting client")
    download(args.host[0],args.port[0],args.dst[0],args.name[0],args.stop_and_wait)
    logging.info("End of execution")