import json
from app.common.youngs_client import YoungsClient
from app.helper.redis_helper import youngs_redis
from config.constants import Constants

class WitalkieClient(YoungsClient):
    def __init__(self, client_protocol):
        super().__init__(client_protocol)
        self.lecture_id = None
        self.status = None
        self.userid = None
        self.is_authorized = False
        self.pid = 0
        self.auth_key = None

    def get_userid(self):
        return self.userid

    def _set_lecture_id(self):
        lecture_id = youngs_redis.hget(self.auth_key, 'lecture_id')
        self.lecture_id = lecture_id.decode('utf-8') if lecture_id is not None else None

    def auth_client(self, token):
        auth_key = str('auth:token:' + token.decode('utf-8'))
        self.auth_key = auth_key
        if youngs_redis.exists(auth_key) is True:
            id, lecture_id = youngs_redis.hmget(auth_key, ['id', 'lecture_id'])
            if id is not None:
                self.userid = id.decode('utf-8')
            if lecture_id is not None:

                self.lecture_id = lecture_id.decode('utf-8')
                print('lecture_id set : ' + self.lecture_id)
            self.token = token
            self.is_authorized = True
            return True
        return False

    def set_client_channel(self, lecture_id):
        self.lecture_id = lecture_id
        self.channel = self.protocol.factory.channel_manager.get_channel(lecture_id)

    def get_client_channel(self):
        return self.lecture_id

    def is_occupying(self):
        print(self.userid)
        self._set_lecture_id()
        occupy_key = Constants.redis_youngs_lecture_occupy_key(self.lecture_id)
        print(occupy_key)
        res = youngs_redis.get(occupy_key)
        print(res)
        if res is None:
            return False
        if self.userid == res.decode('utf-8'):
            print(self.userid + " is occupying")
            return True
        return False
