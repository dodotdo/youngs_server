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
        redis_res = youngs_redis.hmget(Constants.redis_youngs_lecture_occupy_key(self.id), ['occupier'])
        if redis_res is None or len(redis_res) == 0:
            return None
        else:
            occupier = redis_res[0]
            return occupier

    def is_released(self):
        return False if youngs_redis.exists(Constants.redis_youngs_lecture_occupy_key(self.id)) else True

    def request_occupy(self, userid):
        if not self.is_released():
            return False

        redis_mapping = {
            'state': 'locked',
            'occupier': userid.decode('utf-8')
        }
        pipe = youngs_redis.pipeline()
        pipe.hmset(Constants.redis_youngs_lecture_occupy_key(self.id), redis_mapping)
        pipe.expire(Constants.redis_youngs_lecture_occupy_key(self.id), 30)
        pipe.execute()
        return True

    def release(self, userid):
        if not youngs_redis.exists(Constants.redis_youngs_lecture_occupy_key(self.id)):
            return False
        else:
            youngs_redis.delete(Constants.redis_youngs_lecture_occupy_key(self.id))
            return True


    def add_listener(self, userid):
        # if not youngs_redis.sismember(Constants.redis_youngs_lecture_listener_key(self.id), userid):
        #     # Client is not a member of the channel
        #     return False
        res = youngs_redis.sadd(Constants.redis_youngs_lecture_listener_key, userid)
        self.listener_set.add(userid)
        return True #if res == 1 else False

    def remove_listener(self, userid):
        res = youngs_redis.srem(Constants.redis_youngs_lecture_listener_key, userid)
        self.listener_set.remove(userid)
        return True if res == 1 else False


    def get_listeners(self):
        return self.listener_set





