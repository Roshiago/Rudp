from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader

# This segment should be with data, when it's possible.
# Combine with ACK

class NUL(BasicSegment):

    def __init__(self, seq_num, ack_num):
        super(self)

        # self.addControlBit(ControlBits.ACK)
        # self.addControlBit(ControlBits.NUL)
        
        # self.headerLength(6)
        # self.sequenceNumber(seq_num)
        # self.ackNumber(ack_num)
        
        # self.calc_checksum()