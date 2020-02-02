from components.socket.rudp_socket import RUDPSocket
from components.socket.segments.ACK_SEGMENT import ACK
from components.socket.segments.FactorySegments import FactorySegments
from time import sleep

class Client:
    def __init__(self, addr):
        self._socket = RUDPSocket(addr[0], addr[1])
        self._addr = addr
        self._uuid = None
    
    def connect(self, addr):
        seg_conn = ACK.getDefault()
        data_to_send = ["hello world! this is fine! i work on this rudp, so its just a test, can we send over 128 byte ? I think we can!! just imagine, this is fine".encode('utf-8')]
        seg_conn.data = data_to_send
        data = seg_conn.get_bytes_array(32)

        for pkg in data:
            self._socket.send_to(addr, pkg)

        
        while True:
            seg, addr = self._socket.recv_from()
            print(seg)
            if seg.header.seq_num == 0:
                print("Connection successful! Server:", addr)
                break
    
    def close(self):
        self._socket.close()

