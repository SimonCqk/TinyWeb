def uri_parser(uri: str, cgi_args=None):
    '''
    parse the URL and implement all the WEB-requests strategies.
    :assume: the main directory of static content is `current directory`,
          and main directory of executable files is './cgi-bin'
    '''
    if 'cgi-bin' not in uri:  # static content
        filename = '.' + uri
        if uri.endswith('/'):
            filename += 'home.html'
        return uri, filename, cgi_args, True
    else:  # dynamic content
        try:
            idx = uri.index('?')
        except ValueError:
            idx = None
        if not idx:
            cgi_args = uri[idx + 1:]
        filename = '.' + uri
        return uri, filename, cgi_args, False
