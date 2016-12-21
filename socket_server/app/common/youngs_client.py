from twisted.protocols.basic import LineReceiver

class YoungsClient(LineReceiver):
    def __init__(self, client_protocol):
        self.protocol = client_protocol
        self.token = None
        self.is_authorized = False

    def is_authorized(self):
        return True if self.is_authorized is True else False
