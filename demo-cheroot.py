#!/usr/bin/env python3

from cheroot.wsgi import Server as WSGIServer
from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher

from demo import app, LISTEN_ADDRESS, LISTEN_PORT

if not LISTEN_ADDRESS:
    LISTEN_ADDRESS = "0.0.0.0"

d = WSGIPathInfoDispatcher({'/': app})
server = WSGIServer((LISTEN_ADDRESS, LISTEN_PORT), d)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

