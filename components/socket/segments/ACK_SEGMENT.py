from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader

# This segment should be with data, when it's possible.
class ACK(BasicSegment):

    @staticmethod
    def from_bytes(arr):
        header = arr[0:4] # 4 bytes - header length

        flag = header[0]
        length = header[1]
        seq_num = header[2]
        ack_num = header[3]


        checksum = arr[-2:]
        
        return {
            'header': {
                'flag': flag,
                'length': length,
                'seq_num': seq_num,
                'ack_num': ack_num
            },
            'data': None if len(arr) > 6 else arr[4:-2].decode('utf-8'),
            'checksum': checksum
        }

    def __init__(self, seq_num, ack_num):
        BasicSegment.__init__(self)
        self._header = BaseHeader(ControlBits.ACK, 6, seq_num, ack_num)
        pass
        #self.addControlBit(ControlBits.ACK)
        #self.headerLength(6)
        #self.sequenceNumber(seq_num)
        #self.ackNumber(ack_num)

        #self.calc_checksum()    
    