import argparse
import logging
import lib.constants as constants

import signal

from lib.server import Server


class SignalException(Exception):
    pass


def signal_handler(sig, frame):
    raise SignalException()


def get_args():
    parser = argparse.ArgumentParser(description='Start the fileserver and listen for clients.')
    exclusives = parser.add_mutually_exclusive_group()
    exclusives.add_argument('-v', '--verbose', action='store_true',help='increase output verbosity')
    exclusives.add_argument('-q', '--quiet', action='store_true',help='decrease output verbosity')
    parser.add_argument('-H', '--host', action='store', nargs=1,default=[constants.DEFAULT_HOST],metavar="ADDR",help='specify the service IP address.')
    parser.add_argument('-p', '--port', action='store', nargs=1, default=[constants.DEFAULT_PORT], type=int,help='specify the service port')
    parser.add_argument('-s', '--storage', action='store',nargs=1,help='specify the storage path')
    return parser.parse_args()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = get_args()
    server = None
    try:
        logging.info("Starting server")
        print("Corriendo")
        server = Server(args.host[0],args.port[0])
        server.start_server()
    except SignalException:
        logging.info("Closing server")
    finally:
        if server is not None:
            server.close()
        logging.info("Closed server")

