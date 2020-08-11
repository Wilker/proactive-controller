from utils.log import init_logger
from switch import Switch
import socket

class Controller:
    def __init__(self, address="localhost", port=6653):
        self.address = address
        self.port = port
        self.switches = []
        self.logger = init_logger(__name__, testing_mode=False)


    def await_switch_connection(self):
        switch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        switch_socket.bind((self.address, self.port))
        self.logger.info("Controller Started on port: {}".format(self.port))
        switch_socket.listen(10)
        while True:
            self.logger.info("Listening Connections")
            self.switch_conn, switch_address = switch_socket.accept()
            self.logger.info("New switch Connection from:" + str(switch_address))
            self.switches.append(Switch(self.switch_conn, switch_address).start())

    def start(self):
        self.logger.info("Starting Controller")
        self.await_switch_connection()