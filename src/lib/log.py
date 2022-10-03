import logging


class CustomFormatter(logging.Formatter):

    # COLOUR CONSTANTS
    COLOR_GREEN = '\033[92m'
    COLOR_BLUE = '\033[94m'
    COLOR_RED = '\033[91m'
    COLOR_END = '\033[0m'

    FORMATS = {
        logging.DEBUG: f"%(asctime)s - {COLOR_GREEN} [ %(levelname)s ]\
             {COLOR_END} - %(message)s (%(filename)s:%(lineno)d)",
        logging.INFO: f"%(asctime)s - {COLOR_BLUE} [ %(levelname)s ]\
             {COLOR_END} - %(message)s (%(filename)s:%(lineno)d)",
        logging.ERROR: f"%(asctime)s - {COLOR_RED} [ %(levelname)s ]\
             {COLOR_END} - %(message)s (%(filename)s:%(lineno)d)"}

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


def calculate_verbosity(args):
    if args.verbose is not None:
        return logging.DEBUG
    elif args.quiet is not None:
        return logging.ERROR
    else:
        return logging.INFO


def set_up_logger(args, log_name: str):
    verbosity = calculate_verbosity(args)
    logging.basicConfig(
        filename=log_name,
        level=verbosity,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )

    log = logging.getLogger('')
    ch = logging.StreamHandler()
    ch.setLevel(verbosity)
    ch.setFormatter(CustomFormatter())
    log.addHandler(ch)
