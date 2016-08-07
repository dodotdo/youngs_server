from app.witalkie.client.witalkie_client import WitalkieClient
from app.helper.redis_helper import youngs_redis
from config.constants import Constants

class WitalkieClientManager():

    def __init__(self, app=None):
        self.witalkie_clients = []
        if app is not None:
            app.witalkie_client_manager = self
            self.app = app

    def new_witalkie_connect(self, client):
        self.witalkie_clients.append(WitalkieClient(client))

    def get_witalkie_client(self, client):
        return next((x for x in self.witalkie_clients if x.protocol == client), None)

    def get_witalkie_client_by_userid(self, userid):
        return next((x for x in self.witalkie_clients if x.userid == userid), None)

    def delete_witalkie_client(self, client):
        witalkie_client = next((x for x in self.witalkie_clients if x.protocol == client), None)
        userid = witalkie_client.get_userid()
        res = youngs_redis.srem(Constants.redis_youngs_lecture_listener_key(witalkie_client.lecture_id), userid)
        youngs_redis.delete(Constants.redis_youngs_lecture_occupy_key(witalkie_client.lecture_id))
        youngs_redis.delete(Constants.redis_youngs_auth_token)
        self.witalkie_clients.remove(witalkie_client)
        del(witalkie_client)

        return

    def get_witalkie_client_by_lecture_id(self, lecture_id):
        client_list = []
        for each_client in self.witalkie_clients:
            if each_client.lecture_id == lecture_id:
                client_list.append(each_client)
        return client_list
