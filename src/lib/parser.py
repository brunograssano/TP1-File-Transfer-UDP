import argparse
import lib.constants as constants

def common_parser(description : str):
    parser = argparse.ArgumentParser(description=description)
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

    parser.add_argument("-H", "--host", default=[constants.DEFAULT_HOST],
                        metavar="ADDR", help="server IP address")
    parser.add_argument("-p", "--port", type=int,
                        default=[constants.DEFAULT_PORT], help="server port")
    return parser


def server_parser():
    parser = common_parser("description: Starts the server")
    parser.add_argument('-s', '--storage', action='store',nargs=1,help='specify the storage path')
    return parser.parse_args()

def upload_parser():
    parser = common_parser("description: Uploads a file to the server")
    parser.add_argument('-n','--name',nargs=1, dest='name', metavar="FILENAME",action='store',help='file name')
    return parser.parse_args()

def download_parser():
    parser = common_parser("description: Downloads a specific file from the server")
    parser.add_argument("-d", "--dst", default=".",metavar="FILEPATH", help="destination file path")
    parser.add_argument("-n", "--name", default="",metavar="FILENAME", help="file name")
    return parser.parse_args()
