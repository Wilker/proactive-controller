from threading import Thread
from scapy.all import *
from scapy.contrib.openflow import *
from handshaker import Handshaker

class Switch(Thread):
    def __init__(self, switchConn, switchAddr):
        super().__init__()
        self.switchConn = switchConn
        self.switchAddr = switchAddr

    def run(self):
        Handshaker(self.switchConn).doHandShake()
        self.execute()

    def execute(self):
        while True:
            data = self.switchConn.recv(1024)
            if self.__isMessageEchoRequest__(data):
                print("Echo Request Recebido")
                echo_reply = OFPTEchoReply(xid=4294967295).build()
                print("Enviando Echo Reply")
                self.switchConn.sendall(echo_reply)


    def __isMessageEchoRequest__(self,msg):
        try:
            if (OpenFlow(msg).type == 2):
                return True
            else:
                return False
        except Exception as ex:
            # print("Falha na Checacagem de echo request")
            # print(ex)
            pass
