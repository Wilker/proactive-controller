from scapy.all import *
from scapy.contrib.openflow import *
from utils.log import init_logger


class Handshaker():
    def __init__(self, switchConn):
        self.switchConn = switchConn
        self.logger = init_logger(__name__, testing_mode=False)

    def doHandShake(self):
        try:
            self.logger.info("WAITING OPEN_FLOW_HELLO")
            for i in range(0, 10):
                data = self.switchConn.recv(1024)
                OpenFlow(data).show2()
               # if self.__isMessageHello__(data):
                hello = OFPTHello(xid=4294967295).build()
                self.logger.info("SENDING OF_HELLO")
                self.switchConn.sendall(hello)
                self.logger.info("SENDING OF_FEATURE_REQUEST")
                feature_request = OFPTFeaturesRequest(xid=4294967295).build()
                self.switchConn.sendall(feature_request)
                data = self.switchConn.recv(1024)
                if self.__isMessageFeatureReply__(data):
                    self.logger.info("HANDSHAKE FINISHED!")
                    return data
        except Exception as ex:
            self.logger.info(ex)

    def __isMessageHello__(self, msg):
        try:
            self.logger.info(OpenFlow(msg).show2())
            if (OpenFlow(msg).type == 0):
                return True
            else:
                return False
        except Exception as ex:
            self.logger.error("Not hello")
            self.logger.error(ex)

    def __isMessageFeatureReply__(self, msg):
        try:
            if (OpenFlow(msg).type == 6):
                return True
            else:
                return False
        except Exception as ex:
            self.logger.info("Checka se msg e feature reply")
            self.logger.info(ex)
