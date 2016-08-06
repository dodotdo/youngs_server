import time as ptime
import json
import os
from app.helper.wrapper import make_response
from app.hims_factory import WitalkieFactory, ServerFactory
from app.witalkie.witalkie_protocol import WitalkieProtocol
from app.server.server_protocol import ServerProtocol
from config.constants import Constants
from tests.helper.wrapper import make_data
from tests.socket_testcase import SocketTestCase



class WitalkieProtocolTestCase(SocketTestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        with open(os.path.join(self.dummy_dir, 'channel.json')) as data_file:
            self.dummy_channel = json.load(data_file)
        with open(os.path.join(self.dummy_dir, 'employee.json')) as data_file:
            self.dummy_employee = json.load(data_file)

    def auth_manager(self):
        token = self.dummy_employee['dodotdo_host']['token']
        self.youngs_redis.set(token, 'dodotdo_host')
        self._test_200('dodotdo_host', make_data(token, 'auth'))
        return token

    def auth_housekeeper(self):
        token = self.dummy_employee['dodotdo_housekeeper']['token']
        self.youngs_redis.set(token, 'dodotdo_housekeeper')
        self._test_200('dodotdo_housekeeper', make_data(token, 'auth'))
        return token

    def auth_employee(self, token, userid):
        self.youngs_redis.set(token, userid)


    def setUp(self):
        SocketTestCase.setUp(self)
        self.witalkieFactory = WitalkieFactory(WitalkieProtocol, self.witalkie_app)
        self.serverFacotry = ServerFactory(ServerProtocol, self.app)

        self.server = self.serverFacotry.buildProtocol(('127.0.0.1', 0))

        self.clients = {}
        self.createClient('dodotdo_host')

    def test_fail_authorize_token(self):
        self.hash_mod.update((str(ptime.time())).encode())
        token = self.hash_mod.hexdigest()[:10]
        self.youngs_redis.set(token, 'dodotdo_host')
        return self._test_401('dodotdo_host', make_data(token + 'fail', 'auth'))


    def test_fail_select_channel(self):
        token = self.auth_manager()
        self._test_406('dodotdo_host', make_data(token, 'select_channel', {}))
        # self._test_404(make_data(token, 'select_channel', {"channel_id": 1}))

    def test_select_channel(self):
        token = self.auth_manager()
        for each_channel in self.dummy_channel:
            self.youngs_redis.sadd(Constants.REDIS_YOUNGS_LECTURE_LIVE_KEY, each_channel['id'])
            for each_member in each_channel['memberList']:
                self.youngs_redis.sadd(Constants.redis_witalkie_channel_members_key(each_channel['id']), each_member)
            self._test_200('dodotdo_host', make_data(token, 'select_channel', {"channel_id": each_channel['id']}))

    def test_occupy_release_channel(self):
        token = self.auth_manager()
        self.createClient('dodotdo_housekeeper')
        token2 = self.auth_housekeeper()

        for each_channel in self.dummy_channel:
            self.youngs_redis.sadd(Constants.REDIS_YOUNGS_LECTURE_LIVE_KEY, each_channel['id'])
            for each_member in each_channel['memberList']:
                self.youngs_redis.sadd(Constants.redis_witalkie_channel_members_key(each_channel['id']), each_member)
            self._test_200('dodotdo_host', make_data(token, 'select_channel', {"channel_id": each_channel['id']}))
            self._test_200('dodotdo_host', make_data(token, 'request_occupy_channel', {"channel_id": each_channel['id']}))
            self._test_409('dodotdo_housekeeper', make_data(token2, 'request_occupy_channel', {"channel_id": each_channel['id']}))
            self._test_409('dodotdo_host', make_data(token, 'request_occupy_channel', {"channel_id": each_channel['id']}))
            self._test_200('dodotdo_host', make_data(token, 'release_channel', {"channel_id": each_channel['id']}))

    def test_send_voice(self):
        token = self.auth_manager()
        self.createClient('dodotdo_housekeeper')
        token2 = self.auth_housekeeper()

        for each_channel in self.dummy_channel:

            self.youngs_redis.sadd(Constants.REDIS_YOUNGS_LECTURE_LIVE_KEY, each_channel['id'])
            for each_member in each_channel['memberList']:
                self.youngs_redis.sadd(Constants.redis_witalkie_channel_members_key(each_channel['id']), each_member)
            for each_member in each_channel['listening']:
                self._test_200(each_member, make_data(self.dummy_employee[each_member]['token'], 'select_channel', {"channel_id": each_channel['id']}))

            self._test_200('dodotdo_host', make_data(token, 'request_occupy_channel', {"channel_id": each_channel['id']}))

            self.clients['dodotdo_host'].proto.rawDataReceived(make_data(token, 'send_voice', {"channel_id": each_channel['id'], "voice": "hi"}))
            print(self.clients['dodotdo_housekeeper'].transport.stream[0])


