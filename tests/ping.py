import time

from yoko import YokoSync


def main():
    a_addr = ('127.0.0.1', 8520)
    b_addr = ('127.0.0.1', 8521)

    peer_a = YokoSync(a_addr)
    peer_b = YokoSync(b_addr)

    print(f'INFO: peer_a token is {peer_a.get_token()}')
    print(f'INFO: peer_b token is {peer_b.get_token()}')

    peer_a.connect(peer_b.get_token())
    peer_b.connect(peer_a.get_token())

    for _ in range(int(input("Enter num of iters: "))):
        print("="*50)
        print(f'INFO: {peer_a}')
        print(f'INFO: {peer_b}')
        time.sleep(2)