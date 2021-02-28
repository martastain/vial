__all__ = ["Vial"]

import os
import sys
import signal
import inspect
import traceback
import wsgiref.simple_server

from .request import VRequest
from .response import VResponse
from .loginmanager import VialLoginManager


try:
    import nxtools
    has_nxtools = True
except ImportError:
    import logging
    hs_nxtools = False


def format_traceback():
    exc_type, exc_value, tb = sys.exc_info()
    result = "Traceback:\n\n    " +  "    ".join(traceback.format_exception(exc_type, exc_value, tb)[1:])
    return result


class VialRequestHandler(wsgiref.simple_server.WSGIRequestHandler):
    def log_message(self, format, *args):
        if not self.server.log_requests:
            return
        req, resp, _ = args
        self.server.parent.logger.debug(f"[{resp}] {req} from {self.client_address[0]}")


class Vial():
    def __init__(self, app_name="Vial", logger=None, **kwargs):
        # Server settings
        self.settings = {
            "simple_response_always_200" : True
        }
        self.settings.update(kwargs)

        # Default headers
        self.headers = {"Server" : app_name}
        self.response = VResponse(self)
        self.app_name = app_name
        self._logger = logger

    @property
    def logger(self):
        if not self._logger:
            if has_nxtools:
                self._logger = nxtools.logging
                self._logger.show_time = True
            else:
                self._logger = logging.getLogger(self.app_name)
        return self._logger

    def __call__(self, environ, respond):
        request = VRequest(environ)
        try:
            r = self.handle(request)
            if type(r) == tuple and len(r) == 3:
                status, headers, body = r
            elif r is None:
                status, headers, body = self.response(501)
            else:
                self.logger.error(f"Vial.handle returned incorrect type {type(r)} for {request}")
                status, headers, body = self.response(500)
        except Exception:
            if has_nxtools:
                nxtools.log_traceback()
            else:
                self.logger.error(f"Unhandled exception")
                self.logger.debug(format_traceback())
            status, headers, body = self.response(500)

        respond(
            status,
            [(key, str(value)) for key, value in headers.items() if value]
        )
        if request.method == "HEAD":
            yield b""
            return

        if inspect.isgeneratorfunction(body):
            yield from body
        else:
            yield body

    def handle(self, request:VRequest):
        return self.response(501)

    def serve(self, host:str="", port:int=8080, log_requests:bool=True):
        """Start a development server"""
        self.logger.info(f"Starting HTTP server at {host}:{port}")
        server = wsgiref.simple_server.make_server(
                host,
                port,
                self,
                handler_class=VialRequestHandler
        )
        server.parent = self
        server.log_requests = log_requests
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print()
            self.logger.info("Keyboard interrupt. Shutting down...")
            server.server_close()
        # Ensure all child threads are terminated as well
        if os.name == "nt":
            os.kill(os.getpid(), signal.CTRL_BREAK_EVENT)
        else:
            os.kill(os.getpid(), signal.SIGTERM)

