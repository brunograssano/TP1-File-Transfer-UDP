import sys
import logging
import lib.constants as constants
from lib.parser import download_parser
from lib.protocols.stop_and_wait import StopAndWait
from lib.protocols.go_back_n import GoBackN

def get_client(stop_and_wait_mode):
    if stop_and_wait_mode:
        return StopAndWait()
    else:
        return GoBackN()

def main() -> None:
    try:
        

        args = download_parser()
        #args = parser.parse_args()
        print(args)
        
        stop_and_wait_mode = args.stop_and_wait
        # todo chequear que tengo espacio para guardar
        # el archivo que quiero descargar

        # todo validar protocolo
        # todo obtener cliente
        client = get_client(stop_and_wait_mode)
        # todo descargar archivo
        result = client.download_file(
            args.dst, args.name, args.host, args.port)

        sys.exit(result)
    # !manejo errores
    except Exception:
        
        sys.exit(1)


if __name__ == '__main__':
    # args = download_parser()
    # set_up_logger(args, constants.DOWNLOAD_LOG_FILENAME)
    main()
