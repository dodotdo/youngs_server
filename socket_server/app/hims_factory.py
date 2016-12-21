from twisted.internet.protocol import Factory

class ServerFactory(Factory):

    def __init__(self, protocol, app):
        self.protocol = protocol
        self.app = app
        self.count = 0
        self.server = None



class WitalkieFactory(Factory):

    def __init__(self, protocol, witalkie_app):
        self.protocol = protocol
        self.witalkie_client_manager = witalkie_app.witalkie_client_manager
        self.channel_manager = witalkie_app.channel_manager
        self.count = 0
        self.server = None



class EchoFactory(Factory):

    def __init__(self, protocol):
        self.protocol = protocol
        self.count = 0
        self.server = None



