import argparse

parser = argparse.ArgumentParser(description='< command description >')


parser.add_argument('-v','--verbose', dest='verbose', action='store_true',help='increase output verbosity')
    
parser.add_argument('-q','--quiet', dest='quiet', action='store_true',help='decrease output verbosity')

parser.add_argument('-H','--host',nargs=1, dest='host', action='store',help='server IP address')

parser.add_argument('-p','--port',nargs=1, dest='port', action='store',help='server port')

parser.add_argument('-s','--src',nargs=1, dest='src', action='store',help='source file path')

parser.add_argument('-n','--name',nargs=1, dest='name', action='store',help='file name')

args = parser.parse_args()
print(args)