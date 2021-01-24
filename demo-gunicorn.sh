#!/bin/bash

# From https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7 :
# 
# If the application is I/O bounded, the best performance usually comes from using “pseudo-threads” (gevent or asyncio).
# 
# If the application is CPU bounded, it doesn’t matter how many concurrent requests are handled by the application. 
# The only thing that matters is the number of parallel requests. 
# Due to Python’s GIL, threads and “pseudo-threads” cannot run in parallel. 
# The only way to achieve parallelism is to increase workers to the suggested (2*CPU)+1, 
# understanding that the maximum number of parallel requests is the number of cores.


CPU_CORES=$(grep -c ^processor /proc/cpuinfo)
NUM_WORKERS=$(( ($CPU_CORES * 2) + 1))
gunicorn demo:app -w $NUM_WORKERS -b 0.0.0.0:8000