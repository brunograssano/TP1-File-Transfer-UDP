import argparse
from socket import *
import lib.constants as constants

def get_args():
    parser = argparse.ArgumentParser(description='< command description >')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count",help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="count", help="decrease output verbosity")
    parser.add_argument('-H','--host',nargs=1, dest='host', default=[constants.DEFAULT_HOST],metavar="ADDR", action='store',help='server IP address')
    parser.add_argument('-p','--port',nargs=1, dest='port', type=int,default=[constants.DEFAULT_PORT],action='store',help='server port')
    parser.add_argument('-s','--src',nargs=1, dest='src', metavar="FILEPATH",action='store',help='source file path')
    parser.add_argument('-n','--name',nargs=1, dest='name', metavar="FILENAME",action='store',help='file name')
    return parser.parse_args()


def upload(server_name: str, server_port: int):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    while True:
        lowerCase = input("Input lowercase sentence:")
        message = "[CLIENT]: " + lowerCase
        if lowerCase == "q":
            break;
        clientSocket.sendto(message.encode(),(server_name, server_port))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
    clientSocket.close()


if __name__ == '__main__':
    args = get_args()
    upload(args.host[0],args.port[0])