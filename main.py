from scapy.all import *
from utils.log import init_logger
from controller import Controller


def main():
    if len(sys.argv) == 4:
        address = sys.argv[1]
        port = sys.argv[2]
        role = sys.argv[3].lower()

        if role not in ['equal', 'master', 'slave']:
            logger.error("Invalid role!")
            exit(1)

        if role == 'equal':
            role = 1
        elif role == 'master':
            role = 2
        elif role == 'slave':
            role = 3

        c = Controller(address=address, port=port, role_mode=role).start()
    elif len(sys.argv) == 1:
        c = Controller().start()
    else:
        logger.error("Wrong number of args")


if __name__ == "__main__":
    logger = init_logger(__name__, testing_mode=False)
    main()
