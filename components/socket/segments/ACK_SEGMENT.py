from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader, convertFromBytes

# This segment should be with data, when it's possible.
class ACK(BasicSegment):
    @staticmethod
    def getDefault():
        init_dict = {
            'header': BaseHeader(ControlBits.ACK),
            'data': [],
            'Checksum': None
        }
        return ACK(**init_dict)

    @staticmethod
    def from_bytes(arr):
        header = arr[0:4] # 4 bytes - header length

        flag = header[0]
        length = header[1]
        seq_num = header[2]
        ack_num = header[3]

        checksum = convertFromBytes(arr[-2:])
        
        header_dict = {
            'ctrlBits': flag,
            'header_len': length,
            'seq_num': seq_num,
            'ack_num': ack_num    
        }

        init_dict = {
            'header': BaseHeader(**header_dict),
            'data': None if length > 6 else arr[4:-2].decode('utf-8'),
            'Checksum': checksum
        }

        return ACK(**init_dict)

    def __init__(self, **kwargs):
        BasicSegment.__init__(self)
        self.__dict__.update(kwargs)

    def __str__(self):
        return "ACK_SEG: " + str(self.__dict__)
    