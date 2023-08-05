from __future__ import absolute_import

import socket
import ssl

from six.moves.urllib.parse import quote, urlsplit
from tempfile import SpooledTemporaryFile

import six
import os
import time

from certauth.certauth import CertificateAuthority

from wsgiprox.resolvers import FixedResolver

try:
    from geventwebsocket.handler import WebSocketHandler
except:  #pragma: no cover
    WebSocketHandler = object

import logging


# ============================================================================
class WrappedWebSockHandler(WebSocketHandler):
    def __init__(self, connect_handler):
        self.environ = connect_handler.environ
        self.start_response = connect_handler.start_response
        self.request_version = 'HTTP/1.1'
        self._logger = logging.getLogger(__file__)

        self.socket = connect_handler.curr_sock
        self.rfile = connect_handler.reader

        class FakeServer(object):
            def __init__(self):
                self.application = {}

        self.server = FakeServer()

    @property
    def logger(self):
        return self._logger


# ============================================================================
class BaseHandler(object):
    FILTER_REQ_HEADERS = ('HTTP_PROXY_CONNECTION',
                          'HTTP_PROXY_AUTHORIZATION')

    @classmethod
    def chunk_encode(cls, orig_iter):
        for chunk in orig_iter:
            chunk_len = len(chunk)
            if chunk_len:
                yield ('%X\r\n' % chunk_len).encode()
                yield chunk
                yield b'\r\n'

        yield b'0\r\n\r\n'

    @classmethod
    def buffer_iter(cls, orig_iter, buff_size=65536):
        out = SpooledTemporaryFile(buff_size)
        size = 0

        for buff in orig_iter:
            size += len(buff)
            out.write(buff)

        content_length_str = str(size)
        out.seek(0)

        def read_iter():
            while True:
                buff = out.read(buff_size)
                if not buff:
                    break
                yield buff

        return content_length_str, read_iter()


# ============================================================================
class ConnectHandler(BaseHandler):
    def __init__(self, curr_sock, environ, scheme, wsgi, resolve):
        self.curr_sock = curr_sock
        self.environ = environ
        self.scheme = scheme

        self.wsgi = wsgi
        self.resolve = resolve

        self.reader = curr_sock.makefile('rb', -1)

        self._chunk = False
        self._buffer = False
        self.headers_finished = False

        self.convert_env()

    def write(self, data):
        self.finish_headers()
        self.curr_sock.send(data)

    def finish_headers(self):
        if not self.headers_finished:
            self.curr_sock.send(b'\r\n')
            self.headers_finished = True

    def start_response(self, statusline, headers, exc_info=None):
        protocol = self.environ.get('SERVER_PROTOCOL', 'HTTP/1.0')
        status_line = protocol + ' ' + statusline + '\r\n'
        self.curr_sock.send(status_line.encode('iso-8859-1'))

        found_cl = False

        for name, value in headers:
            if not found_cl and name.lower() == 'content-length':
                found_cl = True

            line = name + ': ' + value + '\r\n'
            self.curr_sock.send(line.encode('iso-8859-1'))

        if not found_cl:
            if protocol == 'HTTP/1.1':
                self.curr_sock.send(b'Transfer-Encoding: chunked\r\n')
                self._chunk = True
            else:
                self._buffer = True

        return self.write

    def finish_response(self, raw_sock):
        resp_iter = self.wsgi(self.environ, self.start_response)

        if self._chunk:
            resp_iter = self.chunk_encode(resp_iter)

        elif self._buffer and not self.headers_finished:
            cl, resp_iter = self.buffer_iter(resp_iter)
            self.curr_sock.send(b'Content-Length: ' + cl.encode() + b'\r\n')

        # finish headers after wsgi call
        self.finish_headers()

        for obj in resp_iter:
            if obj:
                self.curr_sock.send(obj)

    def close(self):
        self.reader.close()

    def handle_ws(self):
        ws = WrappedWebSockHandler(self)
        result = ws.upgrade_websocket()

        # start_response() already called in upgrade_websocket()
        # flush headers before starting wsgi
        self.finish_headers()

        # wsgi expected to access established 'wsgi.websocket'

        # do-nothing start-response
        def ignore_sr(s, h, e=None):
            return []

        self.wsgi(self.environ, ignore_sr)

    def convert_env(self):
        statusline = self.reader.readline().rstrip()

        if not statusline:
            statusline = self.reader.readline().rstrip()

        if six.PY3:  #pragma: no cover
            statusline = statusline.decode('iso-8859-1')

        statusparts = statusline.split(' ', 2)
        hostname = self.environ['wsgiprox.connect_host']

        if len(statusparts) < 3:
            raise Exception('Invalid Proxy Request: ' + statusline + ' from ' + hostname)

        self.environ['wsgi.url_scheme'] = self.scheme

        self.environ['REQUEST_METHOD'] = statusparts[0]

        self.environ['SERVER_PROTOCOL'] = statusparts[2].strip()

        full_uri = self.scheme + '://' + hostname + statusparts[1]

        self.resolve(full_uri, self.environ, hostname)

        while True:
            line = self.reader.readline()
            if line:
                line = line.rstrip()
                if six.PY3:  #pragma: no cover
                    line = line.decode('iso-8859-1')

            if not line:
                break

            parts = line.split(':', 1)
            if len(parts) < 2:
                continue

            name = parts[0].strip()
            value = parts[1].strip()

            name = name.replace('-', '_').upper()

            if name not in ('CONTENT_LENGTH', 'CONTENT_TYPE'):
                name = 'HTTP_' + name

            if name not in self.FILTER_REQ_HEADERS:
                self.environ[name] = value

        self.environ['wsgi.input'] = self.reader


# ============================================================================
class HttpProxyHandler(BaseHandler):
    PROXY_CONN_CLOSE = ('Proxy-Connection', 'close')

    def __init__(self, environ, start_response, wsgi, resolve):
        self.environ = environ

        self.real_start_response = start_response

        self.wsgi = wsgi
        self.resolve = resolve

        self.convert_env()

    def convert_env(self):
        full_uri = self.environ['REQUEST_URI']

        parts = urlsplit(full_uri)

        self.resolve(full_uri, self.environ, parts.netloc.split(':')[0])

        for header in list(self.environ.keys()):
            if header in self.FILTER_REQ_HEADERS:
                self.environ.pop(header, '')

    def start_response(self, statusline, headers, exc_info=None):
        headers.append(self.PROXY_CONN_CLOSE)

        return self.real_start_response(statusline, headers, exc_info)

    def __call__(self):
        return self.wsgi(self.environ, self.start_response)


# ============================================================================
class WSGIProxMiddleware(object):
    DEFAULT_HOST = 'wsgiprox'

    CA_ROOT_NAME = 'wsgiprox https proxy CA'

    CA_ROOT_DIR = os.path.join('.', 'ca')

    CA_ROOT_FILE = 'wsgiprox-ca.pem'
    CA_CERTS_DIR = 'certs'

    def __init__(self, wsgi,
                 prefix_resolver=None,
                 download_host=None,
                 proxy_host=None,
                 proxy_options=None,
                 proxy_apps=None):

        self._wsgi = wsgi

        if isinstance(prefix_resolver, str):
            prefix_resolver = FixedResolver(prefix_resolver)

        self.prefix_resolver = prefix_resolver or FixedResolver()

        self.proxy_apps = proxy_apps or {}

        self.proxy_host = proxy_host or self.DEFAULT_HOST

        self.has_sni = hasattr(ssl, 'HAS_SNI') and ssl.HAS_SNI
        self.has_alpn = hasattr(ssl, 'HAS_ALPN') and ssl.HAS_ALPN

        if self.proxy_host not in self.proxy_apps:
            self.proxy_apps[self.proxy_host] = None

        # HTTPS Only Options
        proxy_options = proxy_options or {}

        ca_root_dir = proxy_options.get('ca_root_dir', self.CA_ROOT_DIR)

        ca_file = proxy_options.get('ca_file', self.CA_ROOT_FILE)
        ca_file = os.path.join(ca_root_dir, ca_file)

        # attempt to create the root_ca_file if doesn't exist
        # (generally recommended to create this seperately)
        ca_name = proxy_options.get('ca_name', self.CA_ROOT_NAME)

        certs_dir = proxy_options.get('ca_certs_dir', self.CA_CERTS_DIR)
        certs_dir = os.path.join(ca_root_dir, certs_dir)

        self.ca = CertificateAuthority(ca_file=ca_file,
                                       certs_dir=certs_dir,
                                       ca_name=ca_name,
                                       cert_not_before=-3600)

        self.use_wildcard = proxy_options.get('use_wildcard_certs', True)

        if proxy_options.get('enable_cert_download', True):
            download_host = download_host or self.DEFAULT_HOST
            self.proxy_apps[download_host] = CertDownloader(self.ca)

        self.enable_ws = proxy_options.get('enable_websockets', True)
        if WebSocketHandler == object:
            self.enable_ws = None

    @property
    def root_ca_file(self):
        return self.ca.ca_file

    def wsgi(self, env, start_response):
        # see if the host matches one of the proxy app hosts
        # if so, try to see if there is an wsgi app set
        # and if it returns something
        hostname = env.get('wsgiprox.matched_proxy_host')
        if hostname:
            app = self.proxy_apps.get(hostname)
            if app:
                res = app(env, start_response)
                if res is not None:
                    return res

        # call upstream wsgi app
        return self._wsgi(env, start_response)

    def __call__(self, env, start_response):
        if env['REQUEST_METHOD'] == 'CONNECT':
            return self.handle_connect(env, start_response)
        else:
            self.ensure_request_uri(env)

            if env['REQUEST_URI'].startswith('http://'):
                return self.handle_http_proxy(env, start_response)
            else:
                return self.wsgi(env, start_response)

    def handle_http_proxy(self, env, start_response):
        res = self.require_auth(env, start_response)
        if res is not None:
            return res

        handler = HttpProxyHandler(env, start_response, self.wsgi, self.resolve)
        return handler()

    def handle_connect(self, env, start_response):
        raw_sock = self.get_raw_socket(env)
        if not raw_sock:
            start_response('405 HTTPS Proxy Not Supported',
                           [('Content-Length', '0')])
            return []

        res = self.require_auth(env, start_response)
        if res is not None:
            return res

        connect_handler = None
        curr_sock = None

        try:
            scheme, curr_sock = self.wrap_socket(env, raw_sock)

            connect_handler = ConnectHandler(curr_sock, env, scheme,
                                             self.wsgi, self.resolve)

            # check for websocket upgrade, if enabled
            if self.enable_ws and env.get('HTTP_UPGRADE', '') == 'websocket':
                connect_handler.handle_ws()
            else:
                connect_handler.finish_response(raw_sock)

        except:
            import traceback
            traceback.print_exc()

            start_response('500 Unexpected Error',
                           [('Content-Length', '0')])


        finally:
            if connect_handler:
                connect_handler.close()

            if curr_sock and curr_sock != raw_sock:
                curr_sock.close()

            if env.get('uwsgi.version'):
                start_response('200 OK', [])

        return []

    def _new_context(self):
        context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        if self.has_alpn:
            context.set_alpn_protocols(['http/1.1'])
        return context

    def create_ssl_context(self, hostname):
        if not self.use_wildcard:
            certfile = self.ca.cert_for_host(hostname)
        else:
            certfile = self.ca.get_wildcard_cert(hostname)

        context = self._new_context()
        context.load_cert_chain(certfile)
        return context

    def _get_connect_response(self, env):
        buff = b'\
HTTP/1.0 200 Connection Established\r\n\
Proxy-Connection: close\r\n\
Server: wsgiprox\r\n\
\r\n'
        return buff

    def wrap_socket(self, env, sock):
        host_port = env['PATH_INFO']
        hostname, port = host_port.split(':', 1)
        env['wsgiprox.connect_host'] = hostname

        sock.send(self._get_connect_response(env))

        if port == '80':
            return 'http', sock

        def sni_callback(sock, sni_hostname, orig_context):
            sni_hostname = sni_hostname or hostname
            sock.context = self.create_ssl_context(sni_hostname)
            env['wsgiprox.connect_host'] = sni_hostname

        if self.has_sni:
            context = self._new_context()
            context.set_servername_callback(sni_callback)
        else:
            context = self.create_ssl_context(hostname)

        ssl_sock = context.wrap_socket(sock,
                                       server_side=True,
                                       suppress_ragged_eofs=False,
                                       do_handshake_on_connect=False,
                                      )

        ssl_sock.do_handshake()

        return 'https', ssl_sock

    def require_auth(self, env, start_response):
        if not hasattr(self.prefix_resolver, 'require_auth'):
            return

        auth_req = self.prefix_resolver.require_auth(env)

        if not auth_req:
            return

        auth_req = 'Basic realm="{0}"'.format(auth_req)
        headers = [('Proxy-Authenticate', auth_req),
                   ('Content-Length', '0')]

        start_response('407 Proxy Authentication', headers)
        return []

    def resolve(self, url, env, hostname):
        if hostname in self.proxy_apps.keys():
            parts = urlsplit(url)
            full = parts.path
            if parts.query:
                full += '?' + parts.query

            env['REQUEST_URI'] = full
            env['wsgiprox.matched_proxy_host'] = hostname
            env['wsgiprox.proxy_host'] = hostname
        else:
            env['REQUEST_URI'] = self.prefix_resolver(url, env)
            env['wsgiprox.proxy_host'] = self.proxy_host

        queryparts = env['REQUEST_URI'].split('?', 1)

        env['PATH_INFO'] = queryparts[0]

        env['QUERY_STRING'] = queryparts[1] if len(queryparts) > 1 else ''

    def ensure_request_uri(self, env):
        if 'REQUEST_URI' in env:
            return

        full_uri = env['PATH_INFO']
        if env.get('QUERY_STRING'):
            full_uri += '?' + env['QUERY_STRING']

        env['REQUEST_URI'] = full_uri

    @classmethod
    def get_raw_socket(cls, env):  #pragma: no cover
        sock = None

        if env.get('uwsgi.version'):
            try:
                import uwsgi
                fd = uwsgi.connection_fd()
                sock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
            except Exception as e:
                pass
        elif env.get('gunicorn.socket'):
            sock = env['gunicorn.socket']

        if not sock:
            # attempt to find socket from wsgi.input
            input_ = env.get('wsgi.input')
            if input_:
                if hasattr(input_, '_sock'):
                    raw = input_._sock
                    sock = socket.socket(_sock=raw)
                elif hasattr(input_, 'raw'):
                    sock = input_.raw._sock
                elif hasattr(input_, 'rfile'):
                    # PY3
                    if hasattr(input_.rfile, 'raw'):
                        sock = input_.rfile.raw._sock
                    # PY2
                    else:
                        sock = input_.rfile._sock

        return sock


# ============================================================================
class CertDownloader(object):
    DL_PEM = '/download/pem'
    DL_P12 = '/download/p12'

    def __init__(self, ca):
        self.ca = ca

    def __call__(self, env, start_response):
        path = env.get('PATH_INFO')

        if path == self.DL_PEM:
            buff = b''
            with open(self.ca.ca_file, 'rb') as fh:
                buff = fh.read()

            content_type = 'application/x-x509-ca-cert'

            #buff = buff.split(b'-----END PRIVATE KEY-----')[-1].lstrip()

        elif path == self.DL_P12:
            buff = self.ca.get_root_PKCS12()

            content_type = 'application/x-pkcs12'

        else:
            return None

        headers = [('Content-Length', str(len(buff))),
                   ('Content-Type', content_type)]

        start_response('200 OK', headers)
        return [buff]


