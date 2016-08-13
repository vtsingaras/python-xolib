import websocket
import json
import uuid
import time

class XoError(Exception):
    pass

class XoTimeoutError(Exception):
    pass

class XoApiError(XoError):
    def __init__(self, method, msg):
        self.method = method
        self.msg = msg

class xo:
    ''' xo-server helper class '''
    def __init__(self, server, username=None, password=None, token=None):
        if (server is None):
            raise Exception()
        self._server = server + '/api/'
        self._username = username
        self._password = password
        self._token = token
        self._user = None
        
        self.ws = websocket.WebSocket()
        self.ws.connect(self._server)

    def get_user(self):
        return self._user

    def call (self, method, timeout=10, **kwargs):
        _uuid = uuid.uuid1()
        payload = {
            "method": method,
            "params": kwargs,
            "jsonrpc": "2.0",
            "id": _uuid.hex
        }

        self.ws.send(json.dumps(payload))
        starttime = time.time()
        resp = None
        while time.time() < (starttime + timeout):
            resp = json.loads(self.ws.recv())
            if ( ('id' not in resp) or resp['id'] != _uuid.hex):
                resp = None
                continue
            else:
                if ('error' in resp):
                    raise XoApiError(method, resp['error']['message'])
                break

        if resp is None:
            raise XoTimeoutError
        
        return resp['result']

    def signIn_withPassword(self, email, password):
        return self.call('session.signInWithPassword', email=email, password=password)
    
    def signIn_withToken(self, token):
        return self.call('session.signInWithToken', token=token)
