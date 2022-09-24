import sys
import logging
import lib.constants as constants
import lib.utils as utils
from lib.parser import download_parser
from lib.client.stop_and_wait import StopAndWaitClient
from lib.client.go_back_n import GoBackNClient

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

        parser = download_parser()
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
