from scapy.all import *
from scapy.contrib.openflow3 import *
from arp_processor import ArpProcessor
from utils.log import init_logger
import traceback
from role_manager import RoleManager


class OpenFlowHandler:

    def __init__(self, switch):
        self.switch = switch
        self.logger = init_logger(__name__, testing_mode=False)

    def process_message(self, data):
        if data == b'':
            self.logger.error("socket connection broken")
            raise RuntimeError("socket connection broken")

        if self.__isMessageRoleReply__(data):
            self.logger.info("received OFPT Role Reply")
            self.process_role_reply(data)

        if self.__isMessageEchoRequest__(data):
            self.logger.info("received OFPT Echo Request")
            self.send_echo_reply()

        if self.__isMessagePacketIn__(data):
            self.logger.info("received OFPT Packet IN")
            self.process_packet_in(data)

    def send_echo_reply(self):
        echo_reply = OFPTEchoReply(xid=4294967295).build()
        self.logger.info("sending OFPT Echo Reply")
        self.switch.switchConn.sendall(echo_reply)

    def __isMessageEchoRequest__(self, data):
        try:
            return True if (OpenFlow(data).type == 2) else False
        except Exception as ex:
            self.logger.error(traceback.print_exc())

    def __isMessagePacketIn__(self, data):
        try:
            return True if (OpenFlow(data).type == 10) else False
        except Exception as ex:
            self.logger.error(traceback.print_exc())

    def __isMessageRoleRequest__(self, data):
        try:
            return True if (OpenFlow(data).type == 24) else False
        except Exception as ex:
            self.logger.error(traceback.print_exc())

    def __isMessageRoleReply__(self, data):
        try:
            return True if (OpenFlow(data).type == 25) else False
        except Exception as ex:
            self.logger.error(traceback.print_exc())

    def sendArpToControllerFlowMod(self):
        flowmod = b'\x04\x0e\x00\x60\x00\x00\x00\x02\x00\x01\x00\x00\xea\x6f\x4b\x8e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9c\x40\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x01\x00\x00\x00\x01\x00\x0a\x80\x00\x0a\x02\x08\x06\x00\x00\x00\x00\x00\x00\x00\x05\x00\x08\x00\x00\x00\x00\x00\x04\x00\x18\x00\x00\x00\x00\x00\x00\x00\x10\xff\xff\xff\xfd\xff\xff\x00\x00\x00\x00\x00\x00'
        self.logger.info("sending FlowMod")
        self.switch.switchConn.sendall(flowmod)

    def process_packet_in(self, data):
        packet_in = OpenFlow(data)
        if packet_in.data.name == 'Ethernet':
            payload = packet_in.data.payload
            if payload.name == 'ARP':
                packt_out = ArpProcessor.build_packet_out(packet_in)
                self.logger.info("sending Packet-out")
                self.switch.switchConn.sendall(packt_out.build())

    def process_role_reply(self, data):
        role_reply = OFPTRoleReply(data)
        self.logger.info("switch set to role {}".format(RoleManager.ROLE(role_reply.role).name))
        self.switch.role_manager.role = role_reply.role
