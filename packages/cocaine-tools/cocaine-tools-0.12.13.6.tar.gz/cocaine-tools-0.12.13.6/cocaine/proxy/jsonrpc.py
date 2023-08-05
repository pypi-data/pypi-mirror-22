import json

from tornado import gen
from tornado import httputil

from cocaine.exceptions import ChokeEvent
from cocaine.services import EmptyResponse

from cocaine.proxy.helpers import fill_response_in
from cocaine.proxy.plugin import IPlugin


REQUEST_FIELDS = ('jsonrpc', 'method', 'params', 'id')


class JSONRPC(IPlugin):
    PRIMITIVE = {0: ['value', {}], 1: ['error', {}]}
    STREAMING = {0: ['write', None], 1: ['error', {}], 2: ['close', {}]}

    def __init__(self, proxy, _):
        super(JSONRPC, self).__init__(proxy)
        self._protocols = [
            (lambda tx, rx: rx == {}, self._handle_mute),
            (lambda tx, rx: rx == self.PRIMITIVE, self._handle_primitive),
            (lambda tx, rx: tx == rx == self.STREAMING, self._handle_streaming),
        ]

    @staticmethod
    def name():
        return "jsonrpc"

    def match(self, request):
        return "X-Cocaine-JSON-RPC" in request.headers

    @gen.coroutine
    def process(self, request):
        try:
            payload = json.loads(request.body)
        except ValueError:
            JSONRPC._send_400_error(request, -32700, 'Parse error: Invalid JSON was received by the server.')
            return

        if not all(k in payload for k in REQUEST_FIELDS):
            JSONRPC._send_400_error(request, -32600, 'The JSON sent is not a valid Request object.')
            return

        name, method = payload['method'].split('.', 2)
        args = payload['params']
        chunks = payload.get('chunks', [])
        headers = {}
        if 'authorization' in request.headers:
            headers['authorization'] = request.headers['authorization']

        try:
            service = yield self.proxy.get_service(name, request)
            if service is None:
                JSONRPC._send_500_error(request, payload, 'Service not found.')
                return
        except Exception as err:
            JSONRPC._send_500_error(request, payload, err)
            return

        api = dict((data[0], data) for data in service.api.itervalues())
        if method not in api:
            JSONRPC._send_400_error(request, -32601, 'Method not found.')
            return

        name, tx_tree, rx_tree = api[method]

        try:
            for match, handle in self._protocols:
                if match(tx_tree, rx_tree):
                    result = yield handle(service, method, args, chunks, **headers)
                    break
            else:
                JSONRPC._send_400_error(request, -32000, 'Protocol type is not supported.')
                return
        except Exception as err:
            JSONRPC._send_500_error(request, payload, err)
            return

        headers = httputil.HTTPHeaders({
            'Content-Type': 'application/json-rpc'
        })
        body = {
            'jsonrpc': '2.0',
            'result': result,
            'id': payload['id'],
        }
        fill_response_in(request, 200, 'OK', json.dumps(body), headers)

    @gen.coroutine
    def _handle_mute(self, service, method, args, _, **headers):
        yield getattr(service, method)(*args, **headers)
        return

    @gen.coroutine
    def _handle_primitive(self, service, method, args, _, **headers):
        channel = yield getattr(service, method)(*args, **headers)
        result = yield channel.rx.get()
        raise gen.Return(result)

    @gen.coroutine
    def _handle_streaming(self, service, method, args, chunks, **headers):
        channel = yield getattr(service, method)(*args, **headers)
        for name, data in chunks:
            getattr(channel.tx, name)(*data)

        # TODO: Chunked.
        result = []
        try:
            while True:
                chunk = yield channel.rx.get()

                if not isinstance(chunk, EmptyResponse):
                    result.append(chunk)
        except ChokeEvent:
            pass
        finally:
            if hasattr(channel.tx, 'close'):
                channel.tx.close()

        raise gen.Return(result)

    @staticmethod
    def _send_400_error(request, code, message):
        headers = httputil.HTTPHeaders({'Content-Type': 'application/json-rpc'})
        body = {'code': code, 'message': message}
        fill_response_in(request, 400, 'Bad JSON-RPC request', json.dumps(body), headers)

    @staticmethod
    def _send_500_error(request, payload, err):
        headers = httputil.HTTPHeaders({'Content-Type': 'application/json-rpc'})
        body = {
            'jsonrpc': '2.0',
            'error': str(err),
            'id': payload['id'],
        }
        fill_response_in(request, 500, 'Internal Server Error', json.dumps(body), headers)
