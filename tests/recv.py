import time

from tests.init_peers import init
import threading
import termcolor
import string
import random


def main():
    peer_a, peer_b = init()

    package = {'entropy': ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(
            int(input("Enter len of package: "))
        )
    )}
    send_routine = threading.Thread(target=peer_a.send, args=(package, ))
    send_routine.start()

    status, received_package = peer_b.receive()
    send_routine.join()
    if status is False:
        print(f'[{termcolor.colored('FAILED', color='red')}] Yoko does not work properly')
    else:
        print(f'Yoko received a package: {package}')
        if received_package == package:
            print(f'[{termcolor.colored('SUCCESS', color='green')}] Yoko received a valid package]')
        else:
            print(f'[{termcolor.colored('FAILED', color='red')}] Yoko received a package but with error]')
