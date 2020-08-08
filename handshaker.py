from scapy.all import *
from scapy.contrib.openflow import *


class Handshaker():
    def __init__(self, switchConn):
        self.switchConn = switchConn

    def doHandShake(self):
        try:
            print("Tentando handkshake")
            data = self.switchConn.recv(1024)
            if self.__isMessageHello__(data):
                hello = OFPTHello(xid=4294967295).build()
                print("Enviando hello")
                self.switchConn.sendall(hello)
                print("Enviando features Request")
                feature_request = OFPTFeaturesRequest(xid=4294967295).build()
                self.switchConn.sendall(feature_request)
                data = self.switchConn.recv(1024)
                if self.__isMessageFeatureReply__(data):
                    print("Chegou no fim")
                    return data
        except Exception as ex:
            print(ex)

    def __isMessageHello__(self, msg):
        try:
            if (OpenFlow(msg).type == 0):
                return True
            else:
                return False
        except Exception as ex:
            print("checa se msg e hello")
            print(ex)

    def __isMessageFeatureReply__(selfs, msg):
        try:
            if (OpenFlow(msg).type == 6):
                return True
            else:
                return False
        except Exception as ex:
            print("Checka se msg e feature reply")
            print(ex)