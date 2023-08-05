from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import os
import json
import traceback
import logging
from requests.models import Response
from six import iteritems, string_types
from six.moves.socketserver import ThreadingMixIn
from six.moves.urllib.parse import urlparse
from localstack.config import DEFAULT_ENCODING
from localstack.utils.common import FuncThread
from localstack.utils.compat import bytes_


QUIET = False

# set up logger
LOGGER = logging.getLogger(__name__)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each request in a separate thread."""


class GenericProxyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.proxy = server.my_object
        self.data_bytes = None
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.method = requests.get
        self.forward('GET')

    def do_PUT(self):
        self.data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        self.method = requests.put
        self.forward('PUT')

    def do_POST(self):
        self.data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        self.method = requests.post
        self.forward('POST')

    def do_DELETE(self):
        self.method = requests.delete
        self.forward('DELETE')

    def do_HEAD(self):
        self.method = requests.head
        self.forward('HEAD')

    def do_PATCH(self):
        self.method = requests.patch
        self.data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        self.forward('PATCH')

    def forward(self, method):
        path = self.path
        if '://' in path:
            path = '/' + path.split('://', 1)[1].split('/', 1)[1]
        proxy_url = 'http://%s%s' % (self.proxy.forward_host, path)
        target_url = self.path
        if '://' not in target_url:
            target_url = 'http://%s%s' % (self.proxy.forward_host, target_url)
        data = None
        if method in ['POST', 'PUT', 'PATCH']:
            data_string = self.data_bytes
            try:
                if not isinstance(data_string, string_types):
                    data_string = data_string.decode(DEFAULT_ENCODING)
                data = json.loads(data_string)
            except Exception as e:
                # unable to parse JSON, fallback to verbatim string/bytes
                data = data_string
        proxies = {
            # TODO: check the use of the proxies variable, it doesn't seem to be required anymore
            # 'http': proxy_url,
            # 'https': proxy_url
        }
        forward_headers = dict(self.headers)
        # update original "Host" header
        forward_headers['host'] = urlparse(target_url).netloc
        try:
            response = None
            # update listener (pre-invocation)
            if self.proxy.update_listener:
                do_forward = self.proxy.update_listener(method=method, path=path,
                    data=data, headers=self.headers, return_forward_info=True)
                if isinstance(do_forward, Response):
                    response = do_forward
                elif do_forward is not True:
                    # get status code from response, or use Bad Gateway status code
                    code = do_forward if isinstance(do_forward, int) else 503
                    self.send_response(code)
                    self.end_headers()
                    return
            if response is None:
                response = self.method(proxy_url, data=self.data_bytes,
                    headers=forward_headers, proxies=proxies)
            # update listener (post-invocation)
            if self.proxy.update_listener:
                self.proxy.update_listener(method=method, path=path,
                    data=data, headers=self.headers, response=response)
            # copy headers and return response
            self.send_response(response.status_code)
            for header_key, header_value in iteritems(response.headers):
                self.send_header(header_key, header_value)
            self.end_headers()
            self.wfile.write(bytes_(response.content))
        except Exception as e:
            if not self.proxy.quiet:
                LOGGER.exception("Error forwarding request: %s" % str(e))

    def log_message(self, format, *args):
        return


class GenericProxy(FuncThread):
    def __init__(self, port, forward_host, update_listener=None, quiet=False, params={}):
        FuncThread.__init__(self, self.run_cmd, params, quiet=quiet)
        self.httpd = None
        self.port = port
        self.quiet = quiet
        self.forward_host = forward_host
        self.update_listener = update_listener

    def run_cmd(self, params):
        try:
            self.httpd = ThreadedHTTPServer(("", self.port), GenericProxyHandler)
            self.httpd.my_object = self
            self.httpd.serve_forever()
        except Exception as e:
            if not self.quiet:
                LOGGER.error('Unable to start proxy on port %s: %s' % (self.port, traceback.format_exc()))
            raise

    def stop(self, quiet=False):
        self.quiet = quiet
        if self.httpd:
            self.httpd.server_close()
