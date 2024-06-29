import time

PING   = 'ping'
PONG   = 'pong'
SRP    = 'srp'
MISSED = 'missed'
HEADER = 'header'
CHUNK  = 'chunk'


def ping() -> dict:
    return {
        'class': PING,
    }


def pong() -> dict:
    return {
        'class': PONG,
        'time' : time.time(),
    }


def missed(orders: list[int], hash_):
    return {
        'class': MISSED,
        'orders': orders,
        'hash': hash_,
    }