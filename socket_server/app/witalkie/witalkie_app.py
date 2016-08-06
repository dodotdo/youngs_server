import json
from app.helper.redis_helper import youngs_redis
from app.witalkie.client.witalkie_client_manager import WitalkieClientManager
from app.witalkie.channel.channel_manager import ChannelManager

class WitalkieApp(object):
    """
    This initialize procedure that needs on witalkie
    ChannelManager is for managing witalkie channel
    WitalkieClientManager is for managing witalkie client
    """

    def __init__(self, app):
        self.channel_manager = ChannelManager(app)
        self.witalkie_client_manager = WitalkieClientManager(app)
