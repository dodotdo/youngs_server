import hashlib
import os
import json
from app.hims_app import YoungsApp
from app.inroom.inroom_app import InroomApp
from app.witalkie.witalkie_app import WitalkieApp
from twisted.trial import unittest
from app.helper.redis_helper import youngs_redis
import testing.redis
import redis
from twisted.test import iosim



class TestClient(object):
    def __init__(self, proto, transport):
        self.proto = proto
        self.transport = transport


class SocketTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.base_dir = os.path.dirname(os.getcwd())
        self.test_dir = os.path.join(self.base_dir, 'socket_server/tests')
        self.dummy_dir = os.path.join(self.test_dir, 'dummy')

    def setUp(self):
        app = YoungsApp(__name__)
        self.app = app
        self.witalkie_app = WitalkieApp(app)
        self.inroom_app = InroomApp(app)
        self.hash_mod = hashlib.sha1()
        redis_path = os.path.join(self.base_dir, 'app_server', 'redis-3.2.0', 'src', 'redis-server')
        self.hims_server = testing.redis.RedisServer(port=6379, base_dir=self.base_dir, redis_server=redis_path)
        self.youngs_redis = redis.Redis(host='localhost', port=self.hims_server.settings['port'], db=0)


    def tearDown(self):
        self.hims_server.stop()

    def createClient(self, userid):
        proto = self.witalkieFactory.buildProtocol(('127.0.0.1', 0))
        transport = iosim.FakeTransport(protocol=proto, isServer=False)
        proto.makeConnection(transport)
        if userid in self.clients:
            return None

        self.clients[userid] = TestClient(proto, transport)
        return self.clients[userid]

    def _test_NONE(self, userid, data):
        self.clients[userid].proto.rawDataReceived(data)


    def _test_200(self, userid, data):
        self.clients[userid].proto.rawDataReceived(data)
        status_code = json.loads(self.clients[userid].transport.getOutBuffer().decode('utf-8'))['status_code']
        self.assertEqual(status_code, 200)

    def _test_401(self, userid, data):
        self.clients[userid].proto.dataReceived(data)
        status_code = json.loads(self.clients[userid].transport.getOutBuffer().decode('utf-8'))['status_code']
        self.assertEqual(status_code, 401)


    def _test_404(self, userid, data):
        self.clients[userid].proto.dataReceived(data)
        status_code = json.loads(self.clients[userid].transport.getOutBuffer().decode('utf-8'))['status_code']
        self.assertEqual(status_code, 404)

    def _test_406(self, userid, data):
        self.clients[userid].proto.dataReceived(data)
        status_code = json.loads(self.clients[userid].transport.getOutBuffer().decode('utf-8'))['status_code']
        self.assertEqual(status_code, 406)


    def _test_409(self, userid, data):
        self.clients[userid].proto.dataReceived(data)
        status_code = json.loads(self.clients[userid].transport.getOutBuffer().decode('utf-8'))['status_code']
        self.assertEqual(status_code, 409)