from components.socket.segments.BasicSegment import BasicSegment, ControlBits, BaseHeader

# This segment should be with data, when it's possible.
# Combine with ACK
class EACK(BaseHeader):
    @staticmethod
    def getDefault():
        init_dict = {
            'header': BaseHeader(ControlBits.EACK),
            'data': [],
            'Сhecksum': 0,
            'list_of_seq_numbers': []
        }

        return EACK(**init_dict)
    

    def __init__(self, **kwargs):
        BasicSegment.__init__(self)
        self.__dict__.update(kwargs)