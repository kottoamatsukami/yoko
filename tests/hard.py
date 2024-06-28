import time

from tests.init_peers import init
import threading
import string
import random


def main():
    peer_a, peer_b = init()

    for _ in range(10):
        package = {'entropy': ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(
                50
            )
        )}

        send_routine = threading.Thread(target=peer_a.send, args=(package, ))
        send_routine.start()
        start = time.time()
        status, package = peer_b.receive()
        assert status is True, 'Yoko does not work properly'
        stop  = time.time()

        send_routine.join()
        print(f'received package: {package} in {stop - start} seconds')
