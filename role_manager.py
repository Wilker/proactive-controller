from scapy.contrib.openflow3 import *
from oftp_role_processor import OFTPRoleProcessor
from utils.log import init_logger
from enum import IntEnum
from utils.log import init_logger


class RoleManager:
    class ROLE(IntEnum):
        EQUAL = 1
        MASTER = 2
        SLAVE = 3

    def __init__(self, switch):
        self.switch = switch
        self.seed = 0
        self.logger = init_logger(__name__, testing_mode=False)
        self.role = self.set_role(RoleManager.ROLE.MASTER)


    def set_role(self, role):
        self.seed = OFTPRoleProcessor.new_generation_id(self.seed)
        role_request = OFTPRoleProcessor.build_role_request(role.value, self.seed)
        self.logger.info("sending {} role request".format(role.name))
        self.switch.switchConn.sendall(role_request.build())
        return role
