import time

from tests.init_peers import init
import threading
import string
import random
import termcolor


def main():

    peer_a, peer_b = init()

    package = {'entropy': ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(
            int(input("Enter len of package: "))
        )
    )}
    print(f"INFO: package is {package}")
    recv_routine = threading.Thread(target=peer_b.receive)
    recv_routine.start()

    status = peer_a.send(package)
    recv_routine.join()

    if status is True:
        print(f"[{termcolor.colored('SUCCESS', color='green')}] Yoko works properly")
    else:
        print(f"[{termcolor.colored('FAILED', color='red')}] Yoko works not properly")
