from app.helper.redis_helper import youngs_redis
from config.constants import Constants
from app.witalkie.channel.channel_item import ChannelItem

class ChannelManager(object):
    def __init__(self, app=None):
        self.channel_dict = {}
        channel_set = youngs_redis.smembers(Constants.REDIS_YOUNGS_LECTURE_LIVE_KEY)
        for each_channel_id in channel_set:
            each_channel_id = int(each_channel_id.decode('utf-8'))
            self.channel_dict[each_channel_id] = ChannelItem(each_channel_id)

        if app is not None:
            app.witalkie_channel_manager = self
            self.app = app

    def get_channel(self, channel_id):
        return self.channel_dict[channel_id] if channel_id in self.channel_dict else None

    def add_channel(self, channel_id):
        if channel_id not in self.channel_dict:
            return False
        self.channel_dict[channel_id] = ChannelItem(channel_id)
        return True

