import socket
from typing import Callable, Union, overload
from engine.network.tcp.tcpbase import TCPBase


class TCPClient(TCPBase):
    def __init__(self, host=None, port=None, s=None):
        super().__init__()

        if s is not None:
            self.socket = s
            self.host, self.port = s.getsockname()
            self.is_connected = True
        else:
            if host == "0.0.0.0":
                host = "localhost"

            self.host = host
            self.port = port
            self.is_connected = False

        self.create_socket(s=s)

    def on_connect(self, s):
        raise NotImplementedError("Implement on_connect")

    def on_disconnect(self, s):
        raise NotImplementedError("Implement on_disconnect")

    def handle_exceptional(self, s):
        if s is not self.socket:
            return

        self.inputs.remove(s)
        self.socket.close()
        self.socket = None
        self.is_connected = False

        self.on_disconnect(s)

    def process(self):

        if not self.is_connected:
            self.connect()

        if not self.is_connected:
            return

        super().process()

    def send_msg(self, msg):
        self.send(self.socket, msg)

    def create_socket(self, s=None):
        if s is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s
        self.inputs.append(s)

    def connect(self):
        if self.is_connected:
            return

        if self.socket is None:
            self.create_socket()

        try:
            self.socket.connect((self.host, self.port))
            self.is_connected = True
        except Exception as e:
            # print(str(e))
            return

        self.on_connect(self.socket)
