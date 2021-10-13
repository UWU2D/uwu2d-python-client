import socket
from engine.network.udp.udpbase import UDPBase


class UDPClient(UDPBase):
    def __init__(self, server_ip, server_port, self_port=None):
        super().__init__()

        self.server_ip = server_ip
        self.server_port = server_port
        self.self_port = self_port
        if self.self_port is not None:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            # self.socket.bind(('', self.self_port))
            self.socket.setblocking(False)

    def send_message(self, message):
        self.send_to(self.server_ip, self.server_port, message)

    def process(self):
        super().process()
        if self.self_port:
            self.read()
