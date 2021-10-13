from typing import List
import socket
from engine.network.tcp.tcpbase import TCPBase


class TCPServer(TCPBase):
    def __init__(self, port=None, backlog=64):

        if port is None:
            port = TCPBase.get_open_port()

        # discovery socket
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = TCPBase.get_host_name()

        self.listen_socket.bind((hostname, port))
        self.listen_socket.listen(backlog)
        self.listen_socket.setblocking(False)

        self.left_over_tcp_data = ""

        self.inputs = [self.listen_socket]
        self.exceptionals = [self.listen_socket]

    def handle_readable(self, s):

        if s is self.listen_socket:
            self.__handle_accept(s)
        else:
            super().read(s)

    def handle_exceptional(self, s):

        self.on_disconnect(s)

        if s in self.inputs:
            self.inputs.remove(s)

        s.close()

    def __handle_accept(self, s):
        client_socket, client_info = s.accept()
        self.on_connect(client_socket)
        self.inputs.append(client_socket)
