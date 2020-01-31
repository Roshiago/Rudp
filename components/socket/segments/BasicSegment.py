from enum import IntEnum
from math import floor
import crcmod

crc16 = crcmod.mkCrcFun(0x13D65, 0xFFFF, True, 0xFFFF)

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
        self._controlBits = ctrlBits
        self._headerLength = header_len
        self._sequenceNumber = seq_num
        self._ackNumber = ack_num
    
    def addControlBit(self, bit: ControlBits):
        self._controlBits |= bit

    def removeControlBit(self, bit: ControlBits):
        self._controlBits &= ~bit
    
    def resetControlBit(self):
        self._controlBits = 0

    def sequenceNumber(self, number):
        self._sequenceNumber = number
    
    def headerLength(self, length):
        self._headerLength = length
    
    def ackNumber(self, number):
        self._ackNumber = number

    def getHeader(self):
        bytesarray = bytearray()
        bytesarray.extend(self._controlBits.to_bytes(1, 'big'))
        bytesarray.extend(self._headerLength.to_bytes(1, 'big'))
        bytesarray.extend(self._sequenceNumber.to_bytes(1, 'big'))
        bytesarray.extend(self._ackNumber.to_bytes(1, 'big'))

        return bytesarray
    

class BasicSegment:
    def __init__(self):
        self._header = BaseHeader()
        self._data = []
    
    def setData(self, data: list):
        self._data = data.copy()
    # def addControlBit(self, bit: ControlBits):
    #     self.header.addControlBit(bit)
    
    # def removeControlBit(self, bit: ControlBits):
    #     self.header.removeControlBit(bit)
    
    # def resetControlBit(self):
    #     self.header.resetControlBit()

    # def sequenceNumber(self, number):
    #     self.header.sequenceNumber(number)
    
    # def headerLength(self, length):
    #     self.header.headerLength(length)
    
    # def ackNumber(self, number):
    #     self.header.ackNumber(number)

    def get_bytes_array(self, max_length_pkg):        
        data_bytes = bytearray()
        for d in self._data:
            data_bytes.extend(d.to_bytes())


        offset_pkg = len(data_bytes) % max_length_pkg
        nums_of_pkg = floor(len(data_bytes) / max_length_pkg) + 1

        if offset_pkg:
            offset_pkg = max_length_pkg - offset_pkg

        if nums_of_pkg == 1:
            offset_pkg = max_length_pkg

        pkgs = []
        
        index = 1
        next_index = 1
        for i in range(0, len(data_bytes) + offset_pkg, max_length_pkg):
            data = data_bytes[i:i+max_length_pkg]
            len_header = len(data)
            
            next_index = index + 1

            if index == nums_of_pkg:
                next_index = 0
            
            self._header.resetControlBit()
            self._header.addControlBit(ControlBits.ACK)
            self._header.headerLength(len_header + 6)
            self._header.sequenceNumber(next_index)
            self._header.ackNumber(index)
            header = self._header #BaseHeader(ControlBits.ACK, len_header + 6, next_index, index)
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
