import argparse
"""
parser = argparse.ArgumentParser(description='Start the fileserver and listen for clients.')

exclusives = parser.add_mutually_exclusive_group()

parser.add_argument('-h', '--help', action='store_true',
                    help='show this help message and exit')

exclusives.add_argument('-v', '--verbose', action='store_true',
                    help='increase output verbosity')

exclusives.add_argument('-q', '--quiet', action='store_true',
                    help='decrease output verbosity')

parser.add_argument('-H', '--host', action='store', nargs=1,
                    help='specify the service IP address.')

parser.add_argument('-p', '--port', action='store', nargs=1,
                    help='specify the service port')

parser.add_argument('-s', '--storage', action='store',nargs=1,
                    help='specify the storage path')

args = parser.parse_args()
print(args)
"""

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(("", serverPort))
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
