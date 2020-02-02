from socket import socket, AF_INET, SOCK_DGRAM, timeout
from components.socket.segments import FactorySegments
from time import sleep

class RUDPSocket:
    def __init__(self, ip = "127.0.0.1", port = 25565, pkg_length = 64):
        self._pkg_length = pkg_length
        self.config = {}
        self._sockaddr = (ip, port)
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.bind(self._sockaddr)
    
    def port(self):
        return self._sockaddr[1]
    
    def accept(self):
        pass

    def connect(self, addr):
        pass

    def ip(self):
        return self._sockaddr[0]

    def send_to(self, sockaddr, data):
        self._socket.settimeout(10)
        counter = 0
        while True:
            try:
                sleep(0.01)
                self._socket.sendto(data, sockaddr)
                byte_pkg, recv_addr = self._socket.recvfrom(self._pkg_length)
                seg = FactorySegments.FactorySegments.getSegment(byte_pkg)
                print("Msg from: ", recv_addr, "\nData segment: ", seg)
                return
            except timeout as e:
                print(e)
                counter += 1
                if counter > 5:
                    break
            except OSError as e:
                print(e)
                return None
    
    def recv_from(self): # pkg, server_addr
        self._socket.settimeout(10)
        counter = 0
        while True:
            try:
                sleep(0.01)
                byte_pkg, recv_addr = self._socket.recvfrom(self._pkg_length)
                seg = FactorySegments.FactorySegments.getSegment(byte_pkg)
                print("Msg from: ", recv_addr, "\nData segment: ", seg)
                ack = FactorySegments.ACK.getDefault()
                ack.header.ack_num = seg.header.ack_num
                ack.header.seq_num = seg.header.seq_num
                for pkg in ack.get_bytes_array(self._pkg_length):
                    self._socket.sendto(pkg, recv_addr)
                return seg, recv_addr
            except timeout as e:
                print(e)
                counter += 1
                if counter > 5:
                    break
            except OSError as e:
                print(e)
                return None
        
        return None

    def close(self):
        self._socket.close()

    
    