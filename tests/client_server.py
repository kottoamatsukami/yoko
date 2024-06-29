from tests.init_peers import init
from yoko import YokoSync

import _thread as thread
import random
import time


def client_routine(client: YokoSync):
    while True:
        status, package = client.receive()
        if status:
            print(package)
        else:
            print('[STATUS]: CLIENT FAILED')

        time.sleep(random.randint(10, 30) / 100)


def server_routine(server: YokoSync):
    while True:
        package = {
            'desc': 'a simple example of USD/RUB price exchanging',
            'optional': 'hello, World!',
            'price': random.randint(70, 110),
        }
        status = server.send(package)
        if not status:
            print('[STATUS]: SERVER FAILED')
        time.sleep(random.randint(10, 30) / 100)


def main():
    server, client = init()
    thread.start_new_thread(server_routine, (server, ))
    thread.start_new_thread(client_routine, (client, ))
    while True:
        pass
