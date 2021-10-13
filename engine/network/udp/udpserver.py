import socket
from typing import Union

from engine.network.udp.udpbase import UDPBase


class UDPServer(UDPBase):
    def __init__(self, port):
        super().__init__()

        # discovery socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", port))
        self.socket.setblocking(False)

        self.clients = []

    @property
    def host(self):
        return self.socket.getsockname()[0]

    @property
    def port(self):
        return self.socket.getsockname()[1]

    def add_client(self, ip, port):
        self.clients.append((ip, port))

    def remove_client(self, ip, port):
        try:
            self.clients.remove((ip, port))
        except ValueError:
            pass

    def send_all(self, data):
        for client_tuple in self.clients:
            self.send_to(client_tuple[0], client_tuple[1], data)

    def process(self):
        super().process()
        self.read()
