#!/usr/bin/env python3

import time
from vial import Vial

class App(Vial):
    def handle(self, request):
        if request.method == "POST":
            fname = f"/tmp/{int(time.time())}"
            with open(fname, "wb") as f:
                f.write(request.body.raw)

            return self.response.json({
                "message" : "Payload saved to /tmp/",
                "size" : request.length
            })

        time.sleep(.1)
        return self.response.text(f"Requested {request.path}. IDK... i give up", status=404)

app = App()

if __name__ == "__main__":
    app.serve("", 8000)
