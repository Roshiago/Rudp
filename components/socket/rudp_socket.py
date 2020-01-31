from socket import *

class RUDPSocket:
    def __init__(self, ip = "127.0.0.1", port = 25565, pkg_length = 128):
        self._pkg_length = pkg_length
        self._sockaddr = (ip, port)
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.bind(self._sockaddr)
    
    def port(self):
        return self._sockaddr[1]
    
    def ip(self):
        return self._sockaddr[0]

    def send_to(self, ip, port, data):
        sockaddr = (ip, port)
        self._socket.sendto(data, sockaddr)
    
    def recv_from(self): #, ip, port): # pkg, server_addr
        pkg, call_addr = self._socket.recvfrom(self._pkg_length)
        return (pkg, call_addr)

    def close(self):
        self._socket.close()

    
    