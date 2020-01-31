from components.socket.rudp_socket import RUDPSocket
from components.socket.segments.FactorySegments import FactorySegments
from components.socket.segments.SYN_SEGMENT import SYN

class Server:
    def __init__(self, addr=('',25565)):
        self.connections = {}
        self.addr2CI = {}
        self.socket = RUDPSocket(addr[0], addr[1])
    
    def accept(self):
        data, addr = self.socket.recv_from() # get connection

        segment = FactorySegments.getSegment(data) # get segment connection
        print(segment)
        #connection = ACK.from_bytes(data) # restore data from bytes
        syn_seg = SYN() # create sync pkgs 
        arr = syn_seg.get_bytes_array() # convert to bytes

        for pkg in arr:
            self.socket.send_to(addr[0], addr[1], pkg) # send sync pkg

        print(syn_seg.ConnectionIdentifier)

        while True:
            data, addr = self.socket.recv_from()

            segment = FactorySegments.getSegment(data)
            print(segment)
            if segment['header']['seq_num'] == 0:
                break
        
        print('Connection complete! New connection:', addr)
        

        # if connection['data'] and connection['data'] == '200':
        #     self.connections[syn_seg.ConnectionIdentifier] = addr
        #     self.addr2CI[addr] = syn_seg.ConnectionIdentifier


    def disconnect_session(self, id):
        del self.connections[id]


    def close(self):
        self.socket.close()





if __name__ == "__main__":
    pass