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


def srp() -> dict:
    return {
        'class': SRP
    }


def missed(orders: list[int]):
    return {
        'class': MISSED,
        'orders': orders
    }