from enum import IntEnum
from math import floor
import crcmod

crc16 = crcmod.mkCrcFun(0x13D65, 0xFFFF, True, 0xFFFF)

def convertFromBytes(byte_data):
    res = 0
    for part in byte_data:
        res = (res << 8) | part
    
    return res

class ControlBits(IntEnum):
    SYN  = 0b10000000
    ACK  = 0b01000000
    EACK = 0b00100000
    RST  = 0b00010000
    NUL  = 0b00001000
    CHK  = 0b00000100
    TCS  = 0b00000010

class BaseHeader:
    @staticmethod
    def from_bytes(arr):
        return BaseHeader(arr[0], arr[1], arr[2], arr[3])

    def __init__(self, ctrlBits = ControlBits.SYN, header_len = 0, seq_num = 0, ack_num = 0):
        self.ctrlBits = ctrlBits
        self.header_len = header_len
        self.seq_num = seq_num
        self.ack_num = ack_num
    
    def checkBit(self, bit: ControlBits):
        return self.ctrlBits & bit

    def __str__(self):
        return "Header: " + "({},{},{},{})".format(self.ctrlBits, \
            self.header_len, self.seq_num, self.ack_num)

    def __repr__(self):
        return str(self)

    def addControlBit(self, bit: ControlBits):
        self.ctrlBits |= bit

    def removeControlBit(self, bit: ControlBits):
        self.ctrlBits &= ~bit
    
    def resetControlBit(self):
        self.ctrlBits = 0

    def sequenceNumber(self, number):
        self.seq_num = number
    
    def headerLength(self, length):
        self.header_len = length
    
    def ackNumber(self, number):
        self.ack_num = number

    def getHeader(self):
        bytesarray = bytearray()
        bytesarray.extend(self.ctrlBits.to_bytes(1, 'big'))
        bytesarray.extend(self.header_len.to_bytes(1, 'big'))
        bytesarray.extend(self.seq_num.to_bytes(1, 'big'))
        bytesarray.extend(self.ack_num.to_bytes(1, 'big'))

        return bytesarray
    

class BasicSegment:
    def __init__(self):
        self.header = BaseHeader()
        self.data = []
    
    def __str__(self):
        return str(self.header) + "\n" \
            + self.data

    def setData(self, data: list):
        self.data = data.copy()

    def get_bytes_array(self, max_length_pkg):        
        data_bytes = bytearray()
        for d in self.data:
            data_bytes.extend(d)


        offset_pkg = len(data_bytes) % max_length_pkg
        nums_of_pkg = floor(len(data_bytes) / max_length_pkg) + 1

        if offset_pkg:
            offset_pkg = max_length_pkg - offset_pkg


        pkgs = []
        
        index = 1
        next_index = 1
        for i in range(0, len(data_bytes) + offset_pkg if nums_of_pkg > 1 else max_length_pkg, max_length_pkg): # HUINYA!!!!
            data = data_bytes[i:i+max_length_pkg]
            len_header = len(data)
            
            next_index = index + 1

            if index == nums_of_pkg:
                next_index = 0
            
            self.header.resetControlBit()
            self.header.addControlBit(ControlBits.ACK)
            self.header.headerLength(len_header + 6)
            self.header.sequenceNumber(next_index)
            self.header.ackNumber(index)
            header = self.header #BaseHeader(ControlBits.ACK, len_header + 6, next_index, index)
            index += 1
            
            header_bytes = header.getHeader()
            checksum = crc16(header_bytes + data)
            
            pkg = bytearray()
            pkg.extend(header_bytes)

            if len_header:
                pkg.extend(data)
            
            pkg.extend(checksum.to_bytes(2, 'big'))
            pkgs.append(pkg)

        return pkgs
