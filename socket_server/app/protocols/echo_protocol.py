from __future__ import print_function

from twisted.protocols.basic import LineReceiver
from app.helper.wrapper import make_response

class EchoProtocol(LineReceiver):


    def __init__(self):
        self.setRawMode()
        self.cnt = None

    def connectionMade(self):
        """
        Once the connection is made we ask the client how many random integers
        the producer should return.

        """
        self.cnt = 0

        print('Echo Connection made from %s' % self.transport.getPeer())

    def dataReceived(self, data):
        print(len(data))
        with open("hihihi.pcm", "a") as myfile:
            myfile.write(repr(data))

        self.message(data)

    def message(self, message):
        self.transport.write(message)

    def connectionLost(self, reason):
        print('Echo Connection lost from %s' % self.transport.getPeer())
