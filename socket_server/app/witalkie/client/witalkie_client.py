import json
from app.common.youngs_client import YoungsClient
from app.helper.redis_helper import youngs_redis
from config.constants import Constants

class WitalkieClient(YoungsClient):
    def __init__(self, client_protocol):
        super().__init__(client_protocol)
        self.channel_id = None
        self.channel = None
        self.status = None
        self.userid = None

    def get_userid(self):
        return self.userid

    def auth_client(self, token):
        token = 'auth:token:'+token
        if youngs_redis.exists(token):
            res = youngs_redis.get(token)
            self.token = token
            self.is_authorized = True
            self.userid = res
            return True
        return False

    def set_client_channel(self, channel_id):
        self.channel_id = channel_id
        self.channel = self.protocol.factory.channel_manager.get_channel(channel_id)

    def get_client_channel(self):
        return self.channel_id

    def is_occupying(self):
        print('is occupying?')
        if self.channel is None:
            return False
        res = youngs_redis.hmget(Constants.redis_youngs_lecture_occupy_key(self.channel_id), ['occupier'])
        print(res)
        if res is None:
            return False
        occupier = res[0]
        if self.userid == occupier:
            return True
        return False
