from socket import *
import lib.constants as constants
from lib.InitialMessage import InitialMessage
from lib.rdtpstream import RDTPStream
from lib.parser import upload_parser


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
    args = upload_parser()
    upload(args.host[0],args.port[0])