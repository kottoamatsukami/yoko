import time
from yoko import YokoSync
from tests.init_peers import init
import threading
import string
import random
import termcolor


def sender_routine(peer: YokoSync):
    while True:
        package = {'entropy': ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(
                random.randint(500, 1024)
            )
        )}
        peer.send(package)


def main():

    peer_a, peer_b = init()
    server_routine = threading.Thread(target=sender_routine, args=(peer_b, ))
    server_routine.start()
    while True:
        status, package = peer_a.receive()

        if status is True:
            print(f"[{termcolor.colored('SUCCESS', color='green')}]: {package}")
        else:
            print(f"[{termcolor.colored('FAILED', color='red')}] Yoko don't work properly")
