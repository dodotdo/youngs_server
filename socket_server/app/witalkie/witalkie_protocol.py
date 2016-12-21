import json

from app.helper.wrapper import make_response
from app.witalkie.witalkie_router import YoungsRouter
from twisted.internet import interfaces
from twisted.protocols.basic import LineReceiver

class WitalkieProtocol(LineReceiver):
    """
    Serve up Talk protocol
    """
    def __init__(self):
        self.setRawMode()
        self.witalkie_router = YoungsRouter(self)

    def connectionMade(self):
        """
        Witalkie client connected
        """
        print('Witalkie Connection made from %s' % self.transport.getPeer())

        self.factory.witalkie_client_manager.new_witalkie_connect(self)


    @staticmethod
    def unzipServerData(data):
        try:
            data_json = json.loads(data.decode('utf-8'))
            token = data_json['token'] if data_json['token'] is not None else None
            namepace = data_json['namespace'] if data_json['namespace'] is not None else None
            payload = data_json['payload'] if 'payload' in data_json else None
            return token, namepace, payload
        except Exception as e:
            print(e)
            return None, None, None

    def rawDataReceived(self, data):
        """
        This receive data from client. Though this format is json, it could be
        changed to raw padding format for decode efficiency.
        """
        print(len(data))
        data = data.rstrip(b'\n\r')
        self.youngs_client = self.factory.witalkie_client_manager.get_witalkie_client(self)
        if not self.youngs_client.is_authorized:
            auth_res = self.youngs_client.auth_client(data)
            print('auth : ' + str(auth_res))
            if auth_res is False:
                self.transport.loseConnection()
                return
            return

        if self.youngs_client.is_occupying():
            channel_id = self.youngs_client.get_client_channel()
            self.witalkie_router.route('send_voice', channel_id, data)



    def connectionLost(self, reason):
        print('Witalkie Connection lost from %s' % self.transport.getPeer())

        self.factory.witalkie_client_manager.delete_witalkie_client(self)

    def message(self, message):
        self.transport.write(message)

