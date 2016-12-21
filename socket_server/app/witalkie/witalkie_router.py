import json
from app.helper.wrapper import make_response, make_voice_packet
from app.helper.redis_helper import youngs_redis
from config.constants import Constants

class YoungsRouter(object):
    def __init__(self, protocol):
        self.protocol = protocol

    def auth(self, payload):
        self.protocol.message(make_response(200, 'Authorized'))

    def _get_channel(self, payload):
        if 'channel_id' not in payload:
            self.protocol.message(make_response(406, 'channel_id required'))
            return None
        channel_id = payload['channel_id']
        channel = self.protocol.factory.channel_manager.get_channel(channel_id)
        if channel is None:
            self.protocol.message(make_response(404, 'wrong channel id'))
            return None
        return channel

    def _get_channel_by_id(self, channel_id):
        channel = self.protocol.factory.channel_manager.get_channel(channel_id)
        if channel is None:
            self.protocol.message(make_response(404, 'wrong channel id'))
            return None
        return channel

    def _get_listeners_by_channel_id(self, channel_id):
        res = youngs_redis.smembers(Constants.redis_youngs_lecture_listener_key(channel_id))
        return [listener.decode('utf-8') for listener in res] if res is not None else []

    def select_channel(self, payload):
        channel = self._get_channel(payload)
        if channel is None:
            return None

        if not channel.add_listener(self.protocol.youngs_client.userid):
            self.protocol.message(make_response(400, 'Failed to add to channel'))
            return None
        self.protocol.youngs_client.set_client_channel(channel.id)
        for each_client in self.protocol.factory.witalkie_client_manager.witalkie_clients:
            print(each_client)
        self.protocol.message(make_response(200, 'Success'))
        return True

    def request_occupy_channel(self, payload):
        channel = self._get_channel(payload)
        if channel is None:
            return None

        if channel.request_occupy(self.protocol.youngs_client.userid):
            self.protocol.message(make_response(200, 'Success', 'request_occupy_channel'))
        else:
            self.protocol.message(make_response(409, 'Already Occupied', 'request_occupy_channel'))


    def release_channel(self, payload):
        channel = self._get_channel(payload)
        if channel is None:
            return None

        if channel.release(self.protocol.youngs_client.userid):
            self.protocol.message(make_response(200, 'Success', 'release_channel'))
        else:
            self.protocol.message(make_response(403, 'Not occupier', 'release_channel'))

    def send_voice(self, channel_id, payload):

        voice = payload
        listeners = self._get_listeners_by_channel_id(channel_id)
        print('listener : ' + str(listeners))
        for each_listener in listeners:
            if each_listener == self.protocol.youngs_client.userid:
                continue
            listener = self.protocol.factory.witalkie_client_manager.get_witalkie_client_by_userid(each_listener)
            print('listening : ' + each_listener)
            listener.protocol.message(make_voice_packet(voice))



    def heart_beat(self, data):
        pass

    def route(self, namespace, *args, **kwargs):
        method = getattr(self, namespace, lambda: None)
        if method is None:
            return None
        return method(*args, **kwargs)
