import sys
import logging
import argparse
import constants

LOGGING_FILE = "logfile_download.txt"

def set_download_parser():
    parser = argparse.ArgumentParser(description="description: Downloads a\
                                     specific file from the server")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count",
                       help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="count",
                       help="decrease output verbosity")
    parser.add_argument("-H", "--host", default=constants.DEFAULT_HOST,
                        metavar="ADDR", help="server IP address")
    parser.add_argument("-p", "--port", type=int,
                        default=constants.DEFAULT_PORT, help="server port")
    parser.add_argument("-d", "--dst", default=".",
                        metavar="FILEPATH", help="destination file path")
    parser.add_argument("-n", "--name", default="",
                        metavar="FILENAME", help="file name")
    return parser

def download_file() -> None:
    #try:
    # Setear Logger
    logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    parser = set_download_parser()
    args = parser.parse_args()
    print(args)
    #! calcular nivel de verbosity
    #! validar protocolo
    #! obtener cliente
    #! descargar archivo
    #! manejar errores
    return


if __name__ == '__main__':
    download_file()