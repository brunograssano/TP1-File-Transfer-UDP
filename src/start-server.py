import logging
import signal
from lib.parser import server_parser
from lib.server import Server


class SignalException(Exception):
    pass


def signal_handler(sig, frame):
    raise SignalException()



if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = server_parser()
    server = None
    try:
        logging.info("Starting server")
        print("Corriendo")
        server = Server(args.host[0],args.port[0],args.storage[0])
        server.start_server()
    except SignalException:
        logging.info("Closing server")
    finally:
        if server is not None:
            server.close()
        logging.info("Closed server")

