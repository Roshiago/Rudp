from components.socket.rudp_socket import RUDPSocket
from components.socket.segments.ACK_SEGMENT import ACK
from components.socket.segments.FactorySegments import FactorySegments

class Client:
    def __init__(self, addr):
        self._socket = RUDPSocket(addr[0], addr[1])
        self._addr = addr
        self._uuid = None
    
    def connect(self, addr):
        seg_conn = ACK(0, 0)
        data = seg_conn.get_bytes_array(128)
        for pkg in data:
            self._socket.send_to(addr[0], addr[1], pkg)
        
        while True:
            data, addr = self._socket.recv_from()
            seg = FactorySegments.getSegment(data)
            print(seg)
            if seg['header']['seq_num'] == 0:
                pkgs = seg_conn.get_bytes_array(128)
                for pkg in pkgs:
                    self._socket.send_to(addr[0], addr[1], pkg)
                
                print("Connection successful! Server:", addr)
                break
    
    def close(self):
        self._socket.close()

