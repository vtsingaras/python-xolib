import websocket
from synthetic import synthesize_property
import six
import json
import uuid
import time
import utils


class XoError(Exception):
    pass


class XoTimeoutError(Exception):
    pass


class XoApiError(XoError):
    def __init__(self, method, msg):
        self.method = method
        self.msg = msg


@synthesize_property('timeout', contract=int, default=10)
class xo:
    """ xo-server helper class """

    def __init__(self, server, email=None, password=None, token=None, learn_methods=True):
        if server is None:
            raise Exception()
        self._server = server + '/api/'
        self._email = email
        self._password = password
        self._token = token

        self._ws = websocket.WebSocket()
        self._ws.connect(self._server)

        if self._email is not None and self._password is not None:
            self.call('session.signInWithPassword', email=self._email, password=self._password)
        elif self._token is not None:
            self.call('session.signInWithToken', token=self._token)

        if learn_methods:
            self._learn_methods()

    def call(self, method, **kwargs):
        _uuid = uuid.uuid1()
        payload = {
            "method": method,
            "params": kwargs,
            "jsonrpc": "2.0",
            "id": _uuid.hex
        }

        self._ws.send(json.dumps(payload))
        start_time = time.time()
        resp = None
        while time.time() < (start_time + self.timeout):
            resp = json.loads(self._ws.recv())
            if ('id' not in resp) or resp['id'] != _uuid.hex:
                resp = None
                continue
            else:
                if 'error' in resp:
                    raise XoApiError(method, resp['error']['message'])
                break

        if resp is None:
            raise XoTimeoutError

        return resp['result']

    def _learn_methods(self):
        xoa_methods = self.call('system.getMethodsInfo')
        methods = list()
        for xoa_method_name, xoa_method_info in six.iteritems(xoa_methods):
            method_code = utils.render_function(xoa_method_name, xoa_method_info['params'])
            methods.append(method_code)
        for method_code in methods:
            utils.patch_method_in(self, method_code)
        return methods
