import argparse
from socket import *
import lib.constants as constants
from lib.InitialMessage import InitialMessage
from lib.rdtpstream import RDTPStream

def get_args():
    parser = argparse.ArgumentParser(description='< command description >')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count",help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="count", help="decrease output verbosity")
    parser.add_argument('-H','--host',nargs=1, dest='host', default=[''],metavar="ADDR", action='store',help='server IP address')
    parser.add_argument('-p','--port',nargs=1, dest='port', type=int,default=[constants.DEFAULT_PORT],action='store',help='server port')
    parser.add_argument('-s','--src',nargs=1, dest='src', metavar="FILEPATH",action='store',help='source file path')
    parser.add_argument('-n','--name',nargs=1, dest='name', metavar="FILENAME",action='store',help='file name')
    return parser.parse_args()


def upload(server_name: str, server_port: int):
    client_socket = RDTPStream.client_socket(server_name,server_port)
    print("Socket")

    initial_message = InitialMessage(True, 200, 'Test')
    client_socket.send(initial_message.as_bytes(), ("",server_port))
    print("sent")
    response = client_socket.read(2048)
    print(response.decode())

    client_socket.close()


if __name__ == '__main__':
    args = get_args()
    upload(args.host[0],args.port[0])