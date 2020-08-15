from threading import Thread
from scapy.all import *
from scapy.contrib.openflow3 import *
from handshaker import Handshaker
from utils.log import init_logger
from openflowhandler import OpenFlowHandler
from role_manager import RoleManager


class Switch(Thread):
    def __init__(self, switchConn, switchAddr, role):
        super().__init__()
        self.switchConn = switchConn
        self.switchAddr = switchAddr
        self.role = role
        self.role_manager = ''
        self.logger = init_logger(__name__, testing_mode=False)

    def run(self):
        Handshaker(self.switchConn).doHandShake()
        self.execute()

    def execute(self):
        ofhandler = OpenFlowHandler(self)
        ofhandler.sendArpToControllerFlowMod()
        self.role_manager = RoleManager(self, role=self.role)
        while True:
            data = self.switchConn.recv(1024)
            ofhandler.process_message(data)
