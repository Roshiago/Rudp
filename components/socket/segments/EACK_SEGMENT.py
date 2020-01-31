from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader

# This segment should be with data, when it's possible.
# Combine with ACK
class EACK(BaseHeader):

    def __init__(self, seq_num, ack_num, list_of_seq_numbers: list):
        self.sequenceNumber(seq_num)
        self.ackNumber(ack_num)
        self.seq_numbers = list_of_seq_numbers

        # self.addControlBit(ControlBits.ACK)
        # self.addControlBit(ControlBits.EACK)
        # self._data = list_of_seq_numbers.copy()
        # self.headerLength(len(self._data) + 6)
        # self.sequenceNumber(seq_num)
        # self.ackNumber(ack_num)
        

        # self.calc_checksum()