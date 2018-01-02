'''
:include: some tool-functions used by TINY WEB.
'''


def read_request_headers(request: str):
    '''
    :return: processed requests (ignore headers)
    '''


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
    :TODO: send a HTTP response, which contains a local file.
    '''
    pass


def serve_dynamic():
    '''
    :TODO: derive a sub process to run a CGI program and providing kinds of dynamic contents.
    '''
    pass
