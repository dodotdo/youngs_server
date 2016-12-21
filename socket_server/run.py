#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
This is a sample implementation of a Twisted push producer/consumer system. It
consists of a TCP server which asks the user how many random integers they
want, and it sends the result set back to the user, one result per line,
and finally closes the connection.
"""
from app.socket_app import SocketApp
from twisted.internet import reactor

if __name__ == '__main__':
    server = None
    app = SocketApp()
    reactor.listenTCP(8030, app.echoFactory)
    reactor.listenTCP(9000, app.witalkieFactory)
    reactor.listenTCP(8000, app.serverFactory)
    reactor.run()
