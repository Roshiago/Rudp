from enum import IntEnum
from components.rnd_uuid.uuid_32 import uuid4
from components.socket.segments.BasicSegment import \
    BasicSegment, BaseHeader, ControlBits, crc16, convertFromBytes

class OptionFlags(IntEnum):
    NOT_USED = 0
    CHK = 1
    REUSE = 2
#=======================SYN SEGMENT=======================#
class SYN(BasicSegment):

    @staticmethod
    def from_bytes(data):
        header = data[0:4] # 4 bytes - header length

        controlBits = header[0]
        length = header[1]
        seq_num = header[2]
        ack_num = header[3]

        version = data[4] >> 4
        MaximumNumberOfOutStandingSegments = data[5]
        OptionsFlagField = data[6]
        _ = data[7] # 7 byte skiped! This is Spare
        
        MaximumSegmentSize = convertFromBytes(data[8:10])
        RetransmissionTimeoutValue = convertFromBytes(data[10:12])
        CumulativeAckTimeoutValue = convertFromBytes(data[12:14])
        NullSegmentTimeoutValue = convertFromBytes(data[14:16])
        TransferStateTimeoutValue = convertFromBytes(data[16:18])

        MaxRetrans = data[18]
        MaxCumAck = data[19]
        MaxOutOfSeq = data[20]
        MaxAutoReset = data[21]

        CI32 = convertFromBytes(data[22:26])
        
        checksum = convertFromBytes(data[-2:])
        
        header_dict = {
            'ctrlBits': controlBits,
            'header_len': length,
            'seq_num': seq_num,
            'ack_num': ack_num
        }

        init_dict = {
            'header': BaseHeader(**header_dict),
        
            'Version': version,
            'MaximumNumberOfOutStandingSegments': MaximumNumberOfOutStandingSegments,
            'OptionsFlagField': OptionsFlagField,
            'MaximumSegmentSize': MaximumSegmentSize,
            'RetransmissionTimeoutValue': RetransmissionTimeoutValue,
            'CumulativeAckTimeoutValue': CumulativeAckTimeoutValue,
            'NullSegmentTimeoutValue': NullSegmentTimeoutValue,
            'TransferStateTimeoutValue': TransferStateTimeoutValue,
            'MaxRetrans': MaxRetrans,
            'MaxCumAck': MaxCumAck,
            'MaxOutOfSeq': MaxOutOfSeq,
            'MaxAutoReset': MaxAutoReset,
            'ConnectionIdentifier': CI32,
        
            'Checksum': checksum
        }

        return SYN(**init_dict)

    def __init__(self, **kwargs):
        #self.addControlBit(ControlBits.SYN)
        if not kwargs.get('without_uuid'):
            self.ConnectionIdentifier = uuid4.next()
        else: 
            self.ConnectionIdentifier = 0
        
        self.__dict__.update(kwargs)
    
    def __str__(self):
        return "SYN_SEG: " + str(self.__dict__)

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
        bytesarray.extend(header.getHeader()) # 1-4 bytes
        bytesarray.extend(self.Version.to_bytes(1, 'big')) # 5 byte
        bytesarray.extend(self.MaximumNumberOfOutStandingSegments.to_bytes(1, 'big')) # 6 byte

        bytesarray.extend(self.OptionsFlagField.to_bytes(1, 'big')) # 7 byte
        bytesarray.extend((0).to_bytes(1,'big')) # spare - 8 byte

        bytesarray.extend(self.MaximumSegmentSize.to_bytes(2, 'big')) # 9-10 byte

        bytesarray.extend(self.RetransmissionTimeoutValue.to_bytes(2, 'big')) # 11-12 byte

        bytesarray.extend(self.CumulativeAckTimeoutValue.to_bytes(2, 'big')) # 13-14 byte

        bytesarray.extend(self.NullSegmentTimeoutValue.to_bytes(2, 'big')) # 15-16 byte

        bytesarray.extend(self.TransferStateTimeoutValue.to_bytes(2, 'big')) # 17-18 byte

        bytesarray.extend(self.MaxRetrans.to_bytes(1, 'big')) # 19 byte
        bytesarray.extend(self.MaxCumAck.to_bytes(1, 'big')) # 20 byte

        bytesarray.extend(self.MaxOutOfSeq.to_bytes(1, 'big')) # 21 byte
        bytesarray.extend(self.MaxAutoReset.to_bytes(1, 'big')) # 22 byte

        bytesarray.extend(self.ConnectionIdentifier.to_bytes(4, 'big')) # 23-26 byte

        checksum = crc16(bytesarray) # 27-28 byte

        bytesarray.extend(checksum.to_bytes(2, 'big'))

        return [bytesarray]

#=======================SYN SEGMENT=======================#