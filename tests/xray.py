import string
import random
import time

from tests.init_peers import init
from threading import Thread


def main():
    peer_a, peer_b = init()
    package = {'entropy': ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(
            int(input("Enter len of package: "))
        )
    )}

    receiver = Thread(target=peer_a.send, args=(package, ))
    sender   = Thread(target=peer_b.receive)

    receiver.start()
    sender.start()

    while receiver.is_alive() or sender.is_alive():
        print("="*64)
        print(f"[RECEIVER] [{receiver.is_alive()}]: {peer_a}")
        print(f"[SENDER  ] [{sender.is_alive()}  ]: {peer_b}")

    receiver.join()
    sender.join()

    print('exiting...')
    time.sleep(5)
