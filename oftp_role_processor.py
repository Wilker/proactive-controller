from scapy.contrib.openflow3 import *
from utils.log import init_logger

logger = init_logger(__name__, testing_mode=False)
class OFTPRoleProcessor:

    @staticmethod
    def build_role_request(role, seed):
        return OFPTRoleRequest(version=4,
                               generation_id=seed,
                               role=role)


    @staticmethod
    def new_generation_id(value):
        value += 1
