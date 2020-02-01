from components.socket.segments.ACK_SEGMENT import ACK
from components.socket.segments.EACK_SEGMENT import EACK
from components.socket.segments.SYN_SEGMENT import SYN
from components.socket.segments.NUL_SEGMENT import NUL
from components.socket.segments.RST_SEGMENT import RST
from components.socket.segments.TCS_SEGMENT import TCS

from components.socket.segments.BasicSegment import BaseHeader, ControlBits

segment_map = {
    ControlBits.SYN : SYN,
    ControlBits.ACK : ACK,
    ControlBits.EACK : EACK,
    ControlBits.NUL : NUL,
    ControlBits.RST : RST,
    ControlBits.TCS : TCS
}

class FactorySegments:
    @staticmethod
    def getSegment(data):
        header = BaseHeader.from_bytes(data)
        return segment_map[header.ctrlBits].from_bytes(data)