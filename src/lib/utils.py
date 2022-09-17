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


def print_unknown_exception_catch(logging_file_name):
    logging.critical(
        f"Client Main Thread - Unknown Error:\n\n{traceback.format_exc()}"
        f"\nExiting program")
    print(
        f"{constants.COLOR_RED}[CRITICAL ERROR]{constants.COLOR_END}"
        f" - Check {logging_file_name} for further details - "
        f"Exiting Program")
