from threading import Thread
from scapy.all import *
from scapy.contrib.openflow3 import *
from handshaker import Handshaker
from utils.log import init_logger
from openflowhandler import OpenFlowHandler


class Switch(Thread):
    def __init__(self, switchConn, switchAddr):
        super().__init__()
        self.switchConn = switchConn
        self.switchAddr = switchAddr
        self.logger = init_logger(__name__, testing_mode=False)

    def run(self):
        Handshaker(self.switchConn).doHandShake()
        self.execute()

    def execute(self):
        ofhandler = OpenFlowHandler(self.switchConn)
        ofhandler.sendArpToControllerFlodMod()
        while True:
            data = self.switchConn.recv(1024)
            ofhandler.process_message(data)
