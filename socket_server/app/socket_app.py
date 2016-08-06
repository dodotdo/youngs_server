from sys import stdout
from app.hims_app import YoungsApp
from app.server.server_protocol import ServerProtocol
from app.witalkie.witalkie_app import WitalkieApp
from app.witalkie.witalkie_protocol import WitalkieProtocol
from twisted.python.log import startLogging
from .hims_factory import ServerFactory, WitalkieFactory


class SocketApp():
    app = YoungsApp(__name__)

    server = None
    witalkie_app = WitalkieApp(app)
    startLogging(stdout)

    serverFactory = ServerFactory(ServerProtocol, app)
    witalkieFactory = WitalkieFactory(WitalkieProtocol, witalkie_app)
