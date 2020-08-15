from utils.log import init_logger
from role_manager import RoleManager
from switch import Switch
import socket


class Controller:
    def __init__(self, address="localhost", port=6653, role_mode=2):
        self.address = address
        self.port = port
        self.switches = []
        self.role_mode = RoleManager.ROLE.get_role_from_value(role_mode)
        self.logger = init_logger(__name__, testing_mode=False)

    def await_switch_connection(self):
        switch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        switch_socket.bind((self.address, int(self.port)))
        self.logger.info("Controller Started on port: {}. On {} mode".format(self.port,
                                                                             self.role_mode.name))
        switch_socket.listen(10)
        while True:
            self.logger.info("Listening Connections")
            self.switch_conn, switch_address = switch_socket.accept()
            self.logger.info("New switch Connection from:" + str(switch_address))
            self.switches.append(Switch(self.switch_conn, switch_address, self.role_mode).start())

    def start(self):
        self.logger.info("Starting Controller")
        self.await_switch_connection()
