import sys
import logging
import argparse
import lib.constants as constants
import lib.utils as utils

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

def main() -> None:
    try:
        # Setear Logger
        logging.basicConfig(filename=constants.LOGGING_FILE, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

        parser = set_download_parser()
        args = parser.parse_args()
        print(args)
        #! calcular nivel de verbosity
        verbosity_level = utils.calculate_verbosity(args)
        print(verbosity_level)
        #! Chequear que tengo espacio para guardar el archivo que quiero descargar
        #! validar protocolo
        #! obtener cliente
        #! descargar archivo
        sys.exit(0)
    #? manejo errores
    except Exception:
        utils.print_unknown_exception_catch(constants.LOGGING_FILE)
        sys.exit(1)
    #return


if __name__ == '__main__':
    main()