'''
main executor of TINY WEB.
'''
import sys
import socket
from concurrent.futures import ThreadPoolExecutor
from handler import handler

HOST = '127.0.0.1'
PORT = 80
ADDRESS = (HOST, PORT)
MAX_INCOME = 10  # max income connection.


def main(argv):
    if len(argv) is not 2:
        print('usage: {} <port>'.format(argv[0]), file=sys.stderr)
        return
    tcp_ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ser_sock.bind(ADDRESS)
    tcp_ser_sock.listen(MAX_INCOME)
    pool = ThreadPoolExecutor(max_workers=MAX_INCOME)
    while True:
        tcp_cli_sock, address = tcp_ser_sock.accept()
        print('Accept connection from ({host},{port})'.format(host=address[0], port=address[1]))
        pool.submit(handler, tcp_cli_sock)
    tcp_ser_sock.close()  # may never execute
    pool.shutdown()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
