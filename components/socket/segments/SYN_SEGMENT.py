from enum import IntEnum
from components.rnd_uuid.uuid_32 import uuid4
from components.socket.segments.BasicSegment import BasicSegment, BaseHeader, ControlBits, crc16

class OptionFlags(IntEnum):
    NOT_USED = 0
    CHK = 1
    REUSE = 2
#=======================SYN SEGMENT=======================#
class SYN(BasicSegment):

    @staticmethod
    def from_bytes(data):
        header = data[0:4] # 4 bytes - header length

        flag = header[0]
        length = header[1]
        seq_num = header[2]
        ack_num = header[3]

        version = data[4] >> 4
        MaximumNumberOfOutStandingSegments = data[5]
        OptionsFlagField = data[5]

        def __convertParts(byte_data):
            res = 0
            for part in byte_data:
                res = (res << 8) | part
            
            return res

        MaximumSegmentSize = __convertParts(data[6:8])
        RetransmissionTimeoutValue = __convertParts(data[8:10])
        CumulativeAckTimeoutValue = __convertParts(data[10:12])
        NullSegmentTimeoutValue = __convertParts(data[12:14])
        TransferStateTimeoutValue = __convertParts(data[14:16])

        MaxRetrans = data[16]
        MaxCumAck = data[17]

        CI32 = __convertParts(data[18:22])
        


        
        checksum = data[-2:]
        
        return {
            'header': {
                'flag': bool(flag),
                'length': length,
                'seq_num': seq_num,
                'ack_num': ack_num
            },
            'syn_data': {
                'version': version,
                'MaximumNumberOfOutStandingSegments': MaximumNumberOfOutStandingSegments,
                'OptionsFlagField': bool(OptionsFlagField),
                'MaximumSegmentSize': MaximumSegmentSize,
                'RetransmissionTimeoutValue': RetransmissionTimeoutValue,
                'CumulativeAckTimeoutValue': CumulativeAckTimeoutValue,
                'NullSegmentTimeoutValue': NullSegmentTimeoutValue,
                'TransferStateTimeoutValue': TransferStateTimeoutValue,
                'MaxRetrans': MaxRetrans,
                'MaxCumAck': MaxCumAck,
                'CI32': CI32,
            },
            'checksum': checksum
        }

    def __init__(self, without_uuid = False):
        #self.addControlBit(ControlBits.SYN)
        if not without_uuid:
            self.ConnectionIdentifier = uuid4.next()
        else: 
            self.ConnectionIdentifier = 0

    Version = 1 # version of protocol

    MaximumNumberOfOutStandingSegments = 15 # max number of package without confirmed

    OptionsFlagField = OptionFlags.CHK

    MaximumSegmentSize = 128 # The maximum number of octets that can be received by the peer sending

    RetransmissionTimeoutValue = 150 # The timeout value for retransmission of unacknowledged packets.  
                                     # This value is specified in milliseconds. Range from 100 to 65536.
    CumulativeAckTimeoutValue = 100 # The timeout value for sending an acknowledgment segment if another segment is not sent.
                                    # This value is specified in milliseconds. Range from 100 to 65536. This value should be smaller
                                    # than the RetransmissionTimeoutValue.

    NullSegmentTimeoutValue = 0 # The timeout value for sending a null segment if a data segment has not been sent.  
                                # Thus, the null segment acts as a keep-alive mechanism.
                                # This value is specified in milliseconds.  Range from 0 to 65536.
                                # A value of 0 disables null segments.

    TransferStateTimeoutValue = 0 # Timeout when data is auto resets
                                # This value is specified in milliseconds.  Range from 0 to 65536.
                                # A value of 0 indicates the connection will be auto-reset immediately.

    MaxRetrans = 10 # The maximum number of times consecutive retransmission(s) will be attempted before the connection 
                    # is considered broken. Range from 0 to 255.  
                    # A value of 0 indicates retransmission should be attempted forever.

    MaxCumAck = 5   # The maximum number of acknowledgments that will be accumulated before sending an acknowledgment
                    # if another segment is not sent. Range from 0 to 255.  A value of 0 indicates an acknowledgment
                    # segment will be send immediately when a data, null, or reset segment is received.

    MaxOutOfSeq = 5 #The maximum number of out of sequence packets that will be accumulated
                    # before an EACK (Extended Acknowledgement) segment is sent. Range from 0 to 255.
                    # A value of 0 indicates an EACK will be sent immediately if an out of order segment is received.

    MaxAutoReset = 1 # The maximum number of consecutive auto reset that will performed before
                     # a connection is reset. Range from 0 to 255.
                     # A value of 0 indicates that an auto reset will not be attempted, the
                     # connection will be reset immediately if an auto reset condition occurs.

    ConnectionIdentifier = 0 # 32 bits of length. Unique number for new connection, saves on both sides. 
                             # When connection is reset, client shall send this number to indicate that reset is 
                             # being performed on the connection.
    
    def get_bytes_array(self):
        header = BaseHeader(ControlBits.SYN, 28, 0, 1)
        bytesarray = bytearray()
        bytesarray.extend(header.getHeader())
        bytesarray.extend(self.Version.to_bytes(1, 'big'))
        bytesarray.extend(self.MaximumNumberOfOutStandingSegments.to_bytes(1, 'big'))

        bytesarray.extend(self.OptionsFlagField.to_bytes(1, 'big'))
        bytesarray.extend((0).to_bytes(1,'big'))

        bytesarray.extend(self.MaximumSegmentSize.to_bytes(2, 'big'))

        bytesarray.extend(self.RetransmissionTimeoutValue.to_bytes(2, 'big'))

        bytesarray.extend(self.CumulativeAckTimeoutValue.to_bytes(2, 'big'))

        bytesarray.extend(self.NullSegmentTimeoutValue.to_bytes(2, 'big'))

        bytesarray.extend(self.TransferStateTimeoutValue.to_bytes(2, 'big'))

        bytesarray.extend(self.MaxRetrans.to_bytes(1, 'big'))
        bytesarray.extend(self.MaxCumAck.to_bytes(1, 'big'))

        bytesarray.extend(self.MaxOutOfSeq.to_bytes(1, 'big'))

        bytesarray.extend(self.ConnectionIdentifier.to_bytes(4, 'big'))

        checksum = crc16(bytesarray)

        bytesarray.extend(checksum.to_bytes(2, 'big'))

        return [bytesarray]

#=======================SYN SEGMENT=======================#