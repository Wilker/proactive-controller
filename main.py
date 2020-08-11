from scapy.all import *
from utils.log import init_logger
from controller import Controller


def main():
    if len(sys.argv) == 3:
        address = sys.argv[1]
        port = sys.argv[2]
        c = Controller(address=address, port=port).start()
    elif len(sys.argv) == 1:
        c = Controller().start()
    else:
        logger.error("Wrong number of args")


if __name__ == "__main__":
    logger = init_logger(__name__, testing_mode=False)
    main()
