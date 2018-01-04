'''
main executor of TINY WEB.
'''
import sys
import socket
import threading
from handler import handler

HOST = '127.0.0.1'
PORT = 80
ADDR = (HOST, PORT)
MAX_INCOME = 10


def main(argv):
    if len(argv) is not 2:
        print('usage: {} <port>'.format(argv[0]), file=sys.stderr)
        return
    tcp_ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ser_sock.bind(ADDR)
    tcp_ser_sock.listen(MAX_INCOME)  # max income connection is 5.
    while True:
        tcp_cli_sock, addr = tcp_ser_sock.accept()
        print('Accept connection from ({host},{port})'.format(addr[0], addr[1]))
        t = threading.Thread(target=handler, args=(tcp_cli_sock))
        t.start()
    tcp_ser_sock.close()  # never execute


if __name__ == '__main__':
    sys.exit(main(sys.argv))
