#!/usr/bin/env python3

import time
from vial import Vial

LISTEN_ADDRESS = ""
LISTEN_PORT = 8000


class App(Vial):
    def handle(self, request):
        if request.method == "POST":
            fname = f"/tmp/{int(time.time())}"
            with open(fname, "wb") as f:
                f.write(request.body.raw)

            return self.response.json({
                "message": "Payload saved to /tmp/",
                "size": request.length
            })

        # UTF-8 text/plain
        if request.path == "/text":
            return self.response.text("Lorem ipsum dolor sit amet")

        # match path /api/article/1234
        if route := request.route("api", "article", "$id:int"):
            # and return a simple json response:
            # {"response" : 200, "message" : "Returned article", "id" : 1234}
            return self.response(200, "Returned article", id=route["id"])

        # No content example (for preflight OPTIONS requests)
        if request.path == "/204":
            return self.response.text(status=204, headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Max-Age": "1728000",
            })

        return self.response(200, "Hello World")


app = App()

if __name__ == "__main__":
    app.serve(LISTEN_ADDRESS, LISTEN_PORT)
