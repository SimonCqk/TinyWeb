'''
:include: some tool-functions used by TINY WEB.
'''
import os
import sys
from socket import socket


def client_error(sock: socket, cause, err_num, short_msg, long_msg):
    '''
    check obvious errors and send reports(HTML file) to client.
    '''
    # build the HTTP response body
    body = '<html><title>Tiny Error</title>' + \
           '<body bgcolor="ffffff">\r\n' + \
           '{0}: {1}\r\n'.format(err_num, short_msg) + \
           '<p>{0}: {1}\r\n'.format(long_msg, cause) + \
           '<hr><em>The Tiny Web Server</em>\r\n'
    # print the HTTP response
    buffer = 'HTTP/1.0 {0} {1}\r\n'.format(err_num, short_msg)
    sock.send(buffer.encode('utf-8'))
    buffer = 'Content-type: text/html\r\n'
    sock.send(buffer.encode('utf-8'))
    buffer = 'Content-length: {0}\r\n\r\n'.format(len(body))
    sock.send(buffer.encode('utf-8'))
    sock.send(body.encode('utf-8'))


def read_request_headers(request: str):
    '''
    read & process requests (ignore headers)
    '''

    def _split_request(req: str):
        lines = req.split('\r\n')
        for l in lines:
            yield l

    for line in _split_request(request):
        print(line, file=sys.stdout)


def get_file_type(filename: str):
    if not isinstance(filename, str):
        raise TypeError('A invalid file name passed in.')
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.gif'):
        return 'image/gif'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.jpeg'):
        return 'image/jpeg'
    else:
        return 'text/plain'


def serve_static(sock: socket, filename):
    '''
    send a HTTP response, which contains a local file.
    '''
    # send response headers to client
    file_type = get_file_type(filename)
    src = open(filename, 'r').read()
    buffer = 'HTTP/1.0 200 OK\r\n' + \
             'Server: Tiny Web Server\r\n' + \
             'Connection: close\r\n' + \
             'Content-length: {}\r\n'.format(len(src)) + \
             'Content-type: {}\r\n\r\n'.format(file_type)
    sock.send(buffer.encode('utf-8'))
    print('Response headers:\n', file=sys.stdout)
    print(buffer)
    # send response body to client
    sock.send(src.encode('utf-8'))


def serve_dynamic(sock: socket, filename, cgi_args):
    '''
    derive a sub process to run a CGI program and providing kinds of dynamic contents.
    '''
    buffer = 'HTTP/1.0 200 OK\r\n'
    sock.send(buffer.encode('utf-8'))
    buffer = 'Server: Tiny Web Server\r\n'
    sock.send(buffer.encode('utf-8'))
    ori_out = sys.stdout
    if os.fork() == 0:  # fork a sub-process to execute
        os.environ['QUERY_STRING'] = cgi_args
        sys.stdout = sock
        os.execve(filename, [], os.environ)
    os.wait()
    sys.stdout = ori_out
