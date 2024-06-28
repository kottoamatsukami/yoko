from tests import ping, recv, hard, send, xray, idle, client_server
import colorama
import os

colorama.init(autoreset=True)

EXAMPLES = {
    'ping' : ping,
    'recv' : recv,
    'send' : send,
    'hard' : hard,
    'xray' : xray,
    'idle' : idle,

    'client_server' : client_server
}

AUTO = None


def main():
    if AUTO is None or AUTO not in EXAMPLES:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{" Enter example order " :=^50}')
            for name in EXAMPLES:
                print('->', name)
            print('->', 'exit')

            menu = input(": ")
            if menu.lower() == 'exit':
                break
            elif menu in EXAMPLES:
                return EXAMPLES[menu].main()
    else:
        EXAMPLES[AUTO].main()


if __name__ == '__main__':
    main()