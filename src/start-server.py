import logging
import signal
import lib.constants as constants
from lib.parser import server_parser
from lib.server import Server
from lib.log import set_up_logger

class SignalException(Exception):
    pass


def signal_handler(sig, frame):
    raise SignalException()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = server_parser()
    set_up_logger(args, constants.SERVER_LOG_FILENAME)
    server = None
    try:
        logging.info("Starting server")
        server = Server(args.host[0],args.port[0],args.storage[0])
        server.start_server()
    except SignalException:
        logging.info("Signal error, closing server")
    finally:
        if server is not None:
            server.close()
        logging.info("Closed server")

