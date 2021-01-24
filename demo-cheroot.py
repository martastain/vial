#!/usr/bin/env python3

from cheroot.wsgi import Server as WSGIServer
from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher

from demo import app

d = WSGIPathInfoDispatcher({'/': app})
server = WSGIServer(('0.0.0.0', 8000), d)

if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()

