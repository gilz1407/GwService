import redis
redisCon=None
def connect():
    global redisCon
    if redisCon is None:
        redisCon = redis.StrictRedis(host='localhost', port=6379)

    return redisCon