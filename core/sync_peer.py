from core.token import *
from core.packages import *
from queue import Queue
from hashlib import sha256

import _thread as thread
import socket
import json
import time
import stun

PING_DELAY_SEC = 1
HIGH_PING     = 1000
RECV_BUFFSIZE = 1024
BUFFER_SIZE   = 256

HASH_PREFIX_SIZE = 10
MAX_PACKAGE_SIZE = 25
MAX_SEND_ATTEMPTS = 5
HEADER_ATTEMPTS   = 5
HEADER_ATTEMPTS_TIMEOUT = 0.1
MISSING_ATTEMPTS  = 5
MISSING_ATTEMPTS_DELAY = 0.05


class YokoSync:

    def __init__(self, bind_addr: tuple[str, int]):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(bind_addr)
        self.bind_addr   = bind_addr
        self.target_addr = None
        self.buffer      = Queue(maxsize=BUFFER_SIZE)

        self._last_pong  = pong()
        self.ping        = float('inf')

        thread.start_new_thread(self.__thread_firewall, ())
        thread.start_new_thread(self.__thread_udphp, ())

    @property
    def is_alive(self):
        return self.target_addr is not None

    def get_token(self) -> str:
        if self.bind_addr[0] == '0.0.0.0':
            _, external_ip, external_port = stun.get_ip_info()
            return encode((external_ip, external_port))
        return encode(self.bind_addr)

    def connect(self, token: str):
        self.target_addr = decode(token)

    def disconnect(self):
        self.target_addr = None

    def send(self, package: dict):
        json_package = json.dumps(package).encode('utf-8')
        package_hash = sha256(json_package).hexdigest()[:HASH_PREFIX_SIZE]

        packages = {}
        for order in range(len(json_package) // MAX_PACKAGE_SIZE + (len(json_package) % MAX_PACKAGE_SIZE != 0)):
            chunk = json_package[order * MAX_PACKAGE_SIZE:(order + 1) * MAX_PACKAGE_SIZE].hex()
            packages[order] = {
                'class': CHUNK,
                'chunk': chunk,
                'order': order,
            }

        header = {
            'class': 'header',
            'hash': package_hash,
            'size': len(packages),

            # rules
            'RECV_BUFFSIZE': RECV_BUFFSIZE,
        }
        requested_chunks = {i for i in range(header['size'])}

        self.__send(header)
        while self.is_alive and len(requested_chunks) > 0:
            # emptying buffer
            for _ in range(self.buffer.qsize()):
                package = self.buffer.get()
                if package == srp():
                    return True
                elif package['class'] == MISSED:
                    requested_chunks = set(package['orders'])

            # Send all missed chunks
            for requested in requested_chunks:
                self.__send(packages[requested])
            requested_chunks.clear()

        return len(requested_chunks) == 0

    def receive(self):
        chunks   = {}
        header   = None
        attempts = 0
        while attempts < HEADER_ATTEMPTS and self.is_alive:
            package  = self.buffer.get()
            if package['class'] == HEADER:
                header = package
                break
            elif package['class'] == CHUNK:
                chunks[package['order']] = package
            else:
                self.__put_to_buffer(package)
            attempts += 1

        if header is None:
            return False, {}

        missing = {i for i in range(header['size']) if i not in chunks}

        while self.is_alive:
            #                             | is it necessary? |
            while not self.buffer.empty() and len(missing) > 0:
                package = self.buffer.get()
                if package['class'] == CHUNK and package['order'] in missing:
                    chunks[package['order']] = package
                    missing.remove(package['order'])

            if len(missing) == 0:
                break

            self.__send(missed(orders=list(missing)))

        if len(missing) != 0:
            return False, {}

        self.__send(srp())

        # reconstruct package
        total_package = b''
        for i in range(header['size']):
            total_package += bytes.fromhex(chunks[i]['chunk'])

        try:
            total_package = json.loads(total_package)
            return True, total_package
        except json.JSONDecodeError:
            return False, {}

    def __thread_udphp(self):
        while True:
            if self.target_addr is not None:
                self.__send(ping())
            time.sleep(PING_DELAY_SEC)

    def __thread_firewall(self):
        while True:
            if self.target_addr is None:
                continue  # timeout

            data, address = self.socket.recvfrom(RECV_BUFFSIZE)
            if address != self.target_addr:
                print("[FIREWALL Service]: Unexpected address detected")
                continue
            status, package = self._validate_package(data)
            if not status:
                continue

            if package['class'] == PING:
                self.__send(pong())
            elif package['class'] == PONG:
                current_time = time.time()
                ping_millis = (current_time - package['time']) * 1000
                if ping_millis > HIGH_PING:
                    print(f'[FIREWALL]: Ping is too high: {ping_millis:.3f}/{HIGH_PING:.3f} ms. Disconnected')
                    self.disconnect()
                self.ping = ping_millis
            else:
                self.__put_to_buffer(package)

    def __send(self, package: dict) -> bool:
        if self.target_addr is None:
            return False
        json_package = json.dumps(package).encode('utf-8')
        self.socket.sendto(json_package, self.target_addr)
        return True

    def __put_to_buffer(self, package: dict):
        if self.buffer.full():
            self.buffer.get()
        self.buffer.put(package)

    @staticmethod
    def _validate_package(package: bytes):
        try:
            package = json.loads(package)
        except json.JSONDecodeError:
            return False, {}

        if 'class' not in package:
            return False, {}

        return True, package

    def get_ping(self) -> float:
        return self.ping

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.target_addr}/{self.is_alive}): ping={self.ping:.3f}, buffer={self.buffer.qsize()}"


__all__ = [
    'YokoSync'
]