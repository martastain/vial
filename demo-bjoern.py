#!/usr/bin/env python3

import bjoern

from demo import app

bjoern.run(app, "127.0.0.1", 8000, reuse_port=True)
