import logging
import traceback
import lib.constants as constants


# Calculates the verbosity level.
def calculate_verbosity(args) -> int:
    if args.verbose is not None:
        return 2
    elif args.quiet is not None:
        return 0
    else:
        return 1

def print_connection_refused():
    logging.critical("Client Main Thread - Error: "
                     "Conection to the server was refused"
                     "\nExiting Program")
    print(f"{constants.COLOR_RED}[ERROR]{constants.COLOR_END}"
          " - Connection to the server refused.")


def print_unknown_exception_catch(logging_file_name):
    logging.critical(
        f"Client Main Thread - Unknown Error:\n\n{traceback.format_exc()}"
        f"\nExiting program")
    print(
        f"{constants.COLOR_RED}[CRITICAL ERROR]{constants.COLOR_END}"
        f" - Check {logging_file_name} for further details - "
        f"Exiting Program")

def print_file_not_exists(file_name):
    logging.error(
        f"Client Main Thread - Error: The requested file, {file_name},"
        "does not exist\nExiting Program")
    print(f"{constants.COLOR_RED}[ERROR]{constants.COLOR_END}"
          f" - The requested file {file_name} does not exist - "
          "Exiting Program")

def print_file_exists(file_name, verbosity):
    logging.info(
        f"Client Main Thread - Info: Found file {file_name} on server")
    if verbosity == 2:
        print(f"{constants.COLOR_BLUE}[INFO]{constants.COLOR_END}"
              f" - Found file {file_name} on server. Starting download")

def print_file_not_found_error(file_path):
    logging.error(
        "Client Main Thread - Error: The"
        f"{file_path} does not exist\nExiting Program")
    print(f"{constants.COLOR_RED}[ERROR]{constants.COLOR_END}"
          f" - The file {file_path} does not exist.")