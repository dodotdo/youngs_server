from app.helper.redis_helper import youngs_redis
from config.constants import Constants

class ChannelItem(object):

    def __init__(self, id):
        self.id = id
        self.occupier = None
        self.listener_set = set()
        self.redis_channel_key = 'youngs:channel:' + str(self.id)
        self.redis_channel_occupy_key = self.redis_channel_key + ':occupy'
        self.redis_channel_listener_key = self.redis_channel_key + ':listener'
        self.redis_channel_requester_key = self.redis_channel_key + ':requester'

    def get_occupier(self):
        redis_res = youngs_redis.get(Constants.redis_youngs_lecture_occupy_key(self.id))
        if redis_res is None:
            return None
        else:
            occupier = redis_res
            return occupier

    def is_released(self):
        return False if youngs_redis.exists(Constants.redis_youngs_lecture_occupy_key(self.id)) else True


    def get_listeners(self):
        redis_res = youngs_redis.smembers(Constants.redis_youngs_lecture_listener_key(self.id))
        return [listener_id.decode('utf-8') for listener_id in redis_res]

