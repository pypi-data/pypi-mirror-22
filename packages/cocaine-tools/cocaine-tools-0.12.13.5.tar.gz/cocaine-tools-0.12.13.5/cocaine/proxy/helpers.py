import collections
import hashlib
import json
from operator import xor
import re
import struct

from tornado import httputil

CRLF = '\r\n'

SIZE_OF_CHUNK_FMT = '{:X}' + CRLF
TERM_CHUNK = '0' + CRLF + CRLF

URL_REGEX = re.compile(r"/([^/]*)/([^/?]*)(.*)")

TcpEndpoint = collections.namedtuple('TcpEndpoint', ["host", "port"])


class ProxyInvalidRequest(Exception):
    pass


def load_srw_config(path):
    with open(path, mode='r') as f:
        config = json.load(f)
    return config


class Endpoints(object):
    unix_prefix = "unix://"
    tcp_prefix = "tcp://"

    def __init__(self, endpoints):
        self.unix = []
        self.tcp = []
        for i in endpoints:
            if i.startswith(Endpoints.unix_prefix):
                self.unix.append(i[len(Endpoints.unix_prefix):])
            elif i.startswith(Endpoints.tcp_prefix):
                raw = i[len(Endpoints.tcp_prefix):]
                delim_count = raw.count(":")
                if delim_count == 0:  # no port
                    raise ValueError("Endpoint has to containt host:port: %s" % i)
                elif delim_count == 1:  # ipv4 or hostname
                    host, _, port = raw.partition(":")
                    self.tcp.append(TcpEndpoint(host=host, port=int(port)))
                elif delim_count > 1:  # ipv6
                    host, _, port = raw.rpartition(":")
                    if host[0] != "[" or host[-1] != "]":
                        raise ValueError("Invalid IPv6 address %s" % i)
                    self.tcp.append(TcpEndpoint(host=host.strip("[]"), port=int(port)))
            else:
                raise ValueError("Endpoint has to begin either unix:// or tcp:// %s" % i)


def write_chunked(request, chunk):
    request.connection.write(SIZE_OF_CHUNK_FMT.format(len(chunk)))
    request.connection.write(chunk)
    request.connection.write(CRLF)


def finalize_response(request, code, status):
    request.connection.finish()
    request.logger.info("finish request: %d %s %.2fms",
                        code, status, 1000.0 * request.request_time())


def finalize_chunked_response(request, code, status):
    request.connection.write(TERM_CHUNK)
    finalize_response(request, code, status)


def fill_response_in(request, code, status, message, headers=None, chunked=False):
    headers = headers or httputil.HTTPHeaders()

    if not ("Content-Length" in headers or chunked):
        content_length = str(len(message))
        request.logger.debug("Content-Length header was generated by the proxy: %s", content_length)
        headers.add("Content-Length", content_length)

    headers.add("X-Powered-By", "Cocaine")
    headers["X-XSS-Protection"] = "1; mode=block"

    if not chunked:
        request.logger.debug("Content-Length: %s", headers["Content-Length"])

    if getattr(request, "traceid", None) is not None:
        headers.add("X-Request-Id", request.traceid)

    if request.method == "HEAD":
        message = None

    request.connection.write_headers(
        # start_line
        httputil.ResponseStartLine(request.version, code, status),
        # headers
        headers,
        # data
        message)

    if not chunked:
        finalize_response(request, code, status)


def pack_httprequest(request):
    headers = [(item.key, item.value) for item in request.cookies.itervalues()]
    headers.extend(request.headers.items())
    packed = request.method, request.uri, request.version.split("/")[1], headers, request.body
    return packed


def extract_app_and_event(request):
    if "X-Cocaine-Service" in request.headers and "X-Cocaine-Event" in request.headers:
        request.logger.debug('dispatch by headers')
        name = request.headers['X-Cocaine-Service']
        event = request.headers['X-Cocaine-Event']
        if name == '' or event == '':
            raise ProxyInvalidRequest("Invalid request: empty dispatch headers")
        return name, event

    # it's better to drop this way of dispatch
    # to prevent modification of request.path
    request.logger.debug('dispatch by uri')
    match = URL_REGEX.match(request.uri)
    if match is None:
        raise ProxyInvalidRequest("Invalid request")

    name, event, other = match.groups()
    if name == '' or event == '':
        raise ProxyInvalidRequest("Invalid request")

    # Drop from query appname and event's name
    if not other.startswith('/'):
        other = "/" + other
    request.uri = other
    request.path, _, _ = other.partition("?")
    # one more call of extract_app_and_event will not modify request.path
    request.headers['X-Cocaine-Service'] = name
    request.headers['X-Cocaine-Event'] = event
    return name, event


def parse_locators_endpoints(endpoint):
    host, _, port = endpoint.rpartition(":")
    if host and port:
        try:
            return (host, int(port))
        except ValueError:
            pass

    raise Exception("invalid endpoint: %s" % endpoint)


def upper_bound(l, value):
    lo = 0
    hi = len(l)
    while lo < hi:
        mid = (lo + hi) // 2
        if l[mid][0] < value:
            lo = mid + 1
        else:
            hi = mid
    return lo


def header_to_seed(value):
    m = hashlib.new("md5")
    m.update(value)
    # 4 bytes XOR
    return reduce(xor, struct.unpack("@IIII", m.digest()), 0)
