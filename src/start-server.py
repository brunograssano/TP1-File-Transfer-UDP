import argparse
import threading
import random
import lib.constants as constants
from socket import *

def get_args():
    parser = argparse.ArgumentParser(description='Start the fileserver and listen for clients.')
    exclusives = parser.add_mutually_exclusive_group()
    exclusives.add_argument('-v', '--verbose', action='store_true',help='increase output verbosity')
    exclusives.add_argument('-q', '--quiet', action='store_true',help='decrease output verbosity')
    parser.add_argument('-H', '--host', action='store', nargs=1,default=[constants.DEFAULT_HOST],metavar="ADDR",help='specify the service IP address.')
    parser.add_argument('-p', '--port', action='store', nargs=1, default=[constants.DEFAULT_PORT], type=int,help='specify the service port')
    parser.add_argument('-s', '--storage', action='store',nargs=1,help='specify the storage path')
    return parser.parse_args()



def read_client(client_address):
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.bind(('', 0))
    port = "[SERVER]: " + str(client_socket.getsockname()[1])
    client_socket.sendto(port.encode(), client_address)
    while True:
        message, clientAddress = client_socket.recvfrom(2048)
        print("(message, client): {}, {}".format(message, clientAddress))
        modifiedMessage = "[SERVER]: " +message.upper()
        client_socket.sendto(modifiedMessage.encode(), clientAddress)

def start_server(server_name: str, server_port: int):
    clients = []
    welcoming_socket = socket(AF_INET, SOCK_DGRAM)
    welcoming_socket.bind((server_name, server_port))
    print("The server is ready to receive")
    while True:
        message, clientAddress = welcoming_socket.recvfrom(2048)
        welcoming_socket.sendto(("[SERVER]: " + "antes de cambiar de socket").encode(), clientAddress)
        if message == b'close':
            break;
        clients.append(threading.Thread(target=read_client(clientAddress)).start())

    for client in clients:
        client.join()

if __name__ == '__main__':
    args = get_args()
    start_server(args.host[0],args.port[0])
