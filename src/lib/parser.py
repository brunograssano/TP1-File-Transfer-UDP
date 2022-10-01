import argparse
import lib.constants as constants

def common_parser(description : str):
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count",help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="count",help="decrease output verbosity")

    parser.add_argument("-H", "--host", default=[constants.DEFAULT_HOST],metavar="ADDR", help="server IP address")
    parser.add_argument("-p", "--port", type=int,default=[constants.DEFAULT_PORT], help="server port")
    return parser

def server_parser():
    parser = common_parser("description: Starts the server")
    parser.add_argument('-s', '--storage', action='store',nargs=1, default=[constants.DEFAULT_STORAGE], help='specify the storage path')
    return parser.parse_args()

def client_parser(description):
    parser = common_parser(description)
    group_transfer = parser.add_mutually_exclusive_group()
    group_transfer.add_argument("-saw", "--stop_and_wait",action='store_true', help="choose Stop and Wait transfer")
    group_transfer.add_argument("-gbn", "--go_back_n", help="choose Go Back N transfer")
    parser.add_argument('-n','--name',nargs=1, dest='name', required=True, metavar="FILENAME",action='store',help='file name')
    return parser    

def upload_parser():
    parser = client_parser("description: Uploads a file to the server")
    parser.add_argument('-s','--src',nargs=1, dest='src', default=[constants.DEFAULT_SRC], metavar="FILEPATH",action='store',help='source file path')
    return parser.parse_args()

def download_parser():
    parser =  client_parser("description: Downloads a specific file from the server")
    parser.add_argument("-d", "--dst",nargs=1, dest='dst', default=[constants.DEFAULT_DST],metavar="FILEPATH", help="destination file path")
    return parser.parse_args()
