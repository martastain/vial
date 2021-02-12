#!/usr/bin/env python3

import bjoern

from demo import app, LISTEN_ADDRESS, LISTEN_PORT

bjoern.run(app, LISTEN_ADDRESS, LISTEN_PORT, reuse_port=True)
