from components.socket.rudp_socket import RUDPSocket
from components.socket.segments.FactorySegments import FactorySegments
from components.socket.segments.BasicSegment import ControlBits
from components.socket.segments.SYN_SEGMENT import SYN
from time import sleep

class Server:
    def __init__(self, addr=('',25565)):
        self.socket = RUDPSocket(addr[0], addr[1])
    
    def accept(self, addr, f_seg):
        # data_from_client, addr = self.socket.recv_from() # get connection
        # if data_from_client.header.seq_num != 0:
        full_data = [f_seg.data]
        while True:
            seg, addr = self.socket.recv_from()
            full_data.append(seg.data)
            if seg.header.seq_num == 0:
                break
        syn_seg = SYN() # create sync pkgs 
        arr = syn_seg.get_bytes_array() # convert to bytes

        for pkg in arr:
            self.socket.send_to(addr, pkg) # send sync pkg

        print("UUID =", syn_seg.ConnectionIdentifier)

        print('Connection complete! New connection:', addr)

        return full_data

    def listen(self):
        counter = 0
        while True:
            data_from_client, addr = self.socket.recv_from()
            if data_from_client.header.ctrlBits == ControlBits.ACK:
                print('accept')
                print("".join(self.accept(addr, data_from_client)))

            counter += 1

            if counter > 2:
                break

        pass

    def close(self):
        self.socket.close()





if __name__ == "__main__":
    pass