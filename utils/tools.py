'''
:include: some tool-functions used by TINY WEB.
'''
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
        lines = req.split('\n')
        for line in lines:
            yield line

    buf = next(_split_request(request))
    while buf != '\r\n':
        try:
            buf = next(_split_request(request))
        except StopIteration:
            break
        print(buf, file=sys.stdout)


def get_file_type(fname: str):
    if not isinstance(fname, str):
        raise TypeError('A invalid file name passed in.')
    if fname.endswith('.html'):
        return 'text/html'
    elif fname.endswith('.gif'):
        return 'image/gif'
    elif fname.endswith('.png'):
        return 'image/png'
    elif fname.endswith('.jpeg'):
        return 'image/jpeg'
    else:
        return 'text/plain'


def serve_static():
    '''
    send a HTTP response, which contains a local file.
    '''
    pass


def serve_dynamic():
    '''
    derive a sub process to run a CGI program and providing kinds of dynamic contents.
    '''
    pass
