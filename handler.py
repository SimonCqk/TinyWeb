import os
import stat
from socket import socket
from utils.tools import client_error, read_request_headers, serve_static, serve_dynamic
from utils.uri_parser import uri_parser

BUFFER_SIZE = 65575


def handler(sock: socket):
    '''
    main function to handle one HTTP event.
    '''
    # read request line and headers
    print('Request headers:')
    buffer = sock.recv(BUFFER_SIZE)
    if not buffer:
        return
    method, uri, version = buffer.split(' ')
    if not method.upper() == 'GET':
        client_error(sock, method, '501', 'Not implemented', 'Tiny does not implement this method')
        return
    read_request_headers(buffer)

    # parse URI from GET request
    uri, filename, cgi_args, is_static = uri_parser(uri)
    if not os.path.exists(filename):
        client_error(sock, filename, '404', 'Not found', "Tiny couldn't find the file")
        return
    mode = os.stat(filename).st_mode
    if is_static:
        if not stat.S_ISREG(mode) or not stat.S_IRUSR & mode:
            client_error(sock, filename, '403', 'Forbidden', "Tiny couldn't read the file")
            return
        serve_static(sock, filename)
    else:
        if not stat.S_ISREG(mode) or not stat.S_IXUSR & mode:
            client_error(sock, filename, '403', 'Forbidden', "Tiny couldn't run the CGI program")
            return
        serve_dynamic(sock, filename)
