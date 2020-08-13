from scapy.all import *
from scapy.contrib.openflow3 import *
from utils.log import init_logger
import traceback
from enum import Enum


class ArpProcessor:

    @staticmethod
    def build_packet_out(pkt):
        action_flood = OFPATOutput(type=0,
                                   len=16,
                                   port=0xfffb,
                                   max_len=0)
        return OFPTPacketOut(version=4,
                             type=13,
                             xid=0,
                             buffer_id=0xffffffff,
                             in_port=pkt.match.oxm_fields[0].in_port,
                             actions=[action_flood],
                             data=pkt.data)
