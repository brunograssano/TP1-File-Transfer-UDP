import sys
import logging
import argparse
import lib.constants as constants
import lib.utils as utils

from lib.client.stop_and_wait import StopAndWaitClient
from lib.client.go_back_n import GoBackNClient

def set_download_parser():
    parser = argparse.ArgumentParser(description="description: Downloads a\
                                     specific file from the server")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count",
                       help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="count",
                       help="decrease output verbosity")

    group_transfer = parser.add_mutually_exclusive_group()
    group_transfer.add_argument("-saw", "--stop_and_wait",
                        action='store_true', help="choose stop and wait transfer")
    group_transfer.add_argument("-gbn", "--go_back_n", metavar="GO_BACK_N",
                        help="choose go back N transfer")

    parser.add_argument("-H", "--host", default=constants.DEFAULT_HOST,
                        metavar="ADDR", help="server IP address")
    parser.add_argument("-p", "--port", type=int,
                        default=constants.DEFAULT_PORT, help="server port")
    parser.add_argument("-d", "--dst", default=".",
                        metavar="FILEPATH", help="destination file path")
    parser.add_argument("-n", "--name", default="",
                        metavar="FILENAME", help="file name")
    return parser


def get_client(stop_and_wait_mode, verbosity_level=1):
    if stop_and_wait_mode:
        return StopAndWaitClient(verbosity_level)
    else:
        return GoBackNClient(verbosity_level)

def main() -> None:
    try:
        # Seteo archivo de logs
        logging.basicConfig(
            filename=constants.LOGGING_FILE,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S'
        )

        parser = set_download_parser()
        args = parser.parse_args()
        print(args)
        verbosity_level = utils.calculate_verbosity(args)
        print(verbosity_level)
        stop_and_wait_mode = args.stop_and_wait
        # todo chequear que tengo espacio para guardar
        # el archivo que quiero descargar

        # todo validar protocolo
        # todo obtener cliente
        client = get_client(stop_and_wait_mode, verbosity_level)
        # todo descargar archivo
        result = client.download_file(
            args.dst, args.name, args.host, args.port)

        sys.exit(result)
    # !manejo errores
    except Exception:
        utils.print_unknown_exception_catch(constants.LOGGING_FILE)
        sys.exit(1)


if __name__ == '__main__':
    main()
