from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader

# This segment should be with data, when it's possible.
class TCS(BasicSegment):

    def __init__(self, seq_num, ack_num, unique_number):
        super(self)

        # self.addControlBit(ControlBits.ACK)
        # self.addControlBit(ControlBits.TCS)

        # self.headerLength(12)
        # self.sequenceNumber(seq_num)
        # self.ackNumber(ack_num)
        
        # self.ConnectionIdentifier = unique_number

        # self.calc_checksum()

    SeqAdjFactor = 255

    ConnectionIdentifier = 0 # like in SYN