from yoko import YokoSync
from tests.init_peers import init
from threading import Thread
from queue import Queue

import time
import string
import random

STOP = False
BUFFER = Queue()


def printer():
    while not STOP:
        if BUFFER.empty():
            continue

        print("="*64)
        print(BUFFER.get())


def reader(peer: YokoSync):
    while not STOP:
        status, package = peer.receive()
        if status:
            BUFFER.put(f"received: {peer} {package}")


def writer(peer: YokoSync):
    while not STOP:
        package = {'message': ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(
                random.randint(1, 100)
            )
        )}
        status = peer.send(package)
        if status:
            BUFFER.put(f"sent: {peer} {package}")
        else:
            BUFFER.put(f"failed: {peer} {package}")

        time.sleep(random.randint(100, 300) / 100)


def main():
    global STOP
    foo, bar = init()

    # foo routine
    f_r = Thread(target=reader, args=(foo,))
    f_w = Thread(target=writer, args=(foo,))
    # bar routine
    b_r = Thread(target=reader, args=(bar,))
    b_w = Thread(target=writer, args=(bar,))
    # printer
    p = Thread(target=printer)
    #
    p.start()
    f_r.start()
    f_w.start()
    b_r.start()
    b_w.start()

    #
    input("HINT: press any key to exit\n\n")
    STOP = True

    p.join()
    f_r.join(0.5)
    f_w.join(0.5)
    b_r.join(0.5)
    b_w.join(0.5)
    print('exiting...')
