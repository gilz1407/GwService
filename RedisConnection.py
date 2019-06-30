import os

import redis
redisCon=None
def connect():
    global redisCon
    if redisCon is None:
        redisCon = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")))

    return redisCon