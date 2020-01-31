from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader

# The RST is sent as a separate segment and does not include any data.
# Combine with ACK
class RST(BasicSegment):

    def __init__(self, seq_num, ack_num):
        super(self)

        #self.addControlBit(ControlBits.ACK)
        # self.addControlBit(ControlBits.RST)
        # self.headerLength(6)
        # self.sequenceNumber(seq_num)
        # self.ackNumber(ack_num)
        
        # self.calc_checksum()