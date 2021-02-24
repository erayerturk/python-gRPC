#!/usr/bin/env python
import sys
from rq import Connection, Worker
import redis
import os


# Provide queue names to listen to as arguments to this script,
# similar to rq worker
r = redis.Redis(host=os.environ["REDIS_HOST"])
with Connection(connection = r):
    qs = sys.argv[1:] or [os.environ["RQ_QUEUE"]]

    w = Worker(qs)

    w.work()
