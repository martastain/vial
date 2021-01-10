__all__ = ["UServer"]

import wsgiref.simple_server

from .request import VRequest
from .response import VResponse


class Vial():
    def __init__(self):
        self.response = VResponse()

    def __call__(self, environ, respond):
        request = VRequest(environ)
        response = self.handle(request)
        respond(
            response[0], 
            response[1]
        )
        yield response[2]

    def handle(self, request):
        return self.response.text("Vial.handle is not implemented", 500)

    def serve(self, host="", port="8080"):
        server = wsgiref.simple_server.make_server(host, port, self)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            server.server_close()

