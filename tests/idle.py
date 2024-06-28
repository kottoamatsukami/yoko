import time
from tests.init_peers import init


def main():
    peer_a, peer_b = init()
    sleep = 20
    for i in range(sleep):
        print(f"{i+1}/{sleep}")
        time.sleep(1)
    assert peer_a.is_alive and peer_b.is_alive
    print('Buffers:')
    print(peer_a)
    print(peer_b)
    print('Test passed')
