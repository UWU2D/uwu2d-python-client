import socket
import select
import json
from typing import Union


class TCPBase:
    @staticmethod
    def get_open_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    @staticmethod
    def get_host_name():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        hostname = s.getsockname()[0]
        s.close()
        return hostname

    def __init__(self):
        self.inputs = []
        self.exceptionals = []
        self.left_over_tcp_data = ""

    def handle_readable(self, s):
        self.read(s)

    def handle_exceptional(self, s):
        raise Exception("Implement TCPBase.handle_exceptional")

    def on_read(self, s, data):
        raise Exception("Implement TCPBase.on_read")

    def process(self):

        # figure out who can do what
        try:
            readable, _, exceptional = select.select(
                self.inputs, self.inputs, self.exceptionals, 0
            )
        except Exception as e:
            return

        for s in readable:
            self.handle_readable(s)

        for s in exceptional:
            self.handle_exceptional(s)

    def stop(self):
        for s in self.inputs:
            s.close()

        self.inputs = []
        self.exceptionals = []

    def read(self, s):

        try:
            data = s.recv(4096)
        except Exception:
            self.handle_exceptional(s)
            return

        if data in [None, ""]:
            self.handle_exceptional(s)
            return

        # put it in string form
        try:
            data = data.decode()
        except:
            return

        # if we have left over data from another read attempt, prepend it here
        # if self.left_over_tcp_data != '':
        #    data = self.left_over_tcp_data + data

        # loop until no more data left
        while len(data) > 0:

            # parse through the data, looking for @ symobls
            try:
                size, left_over = data.split("@", 1)
            except:
                return

            try:
                size = int(size)
            except:
                return

            # our size indicates taht the rest of the message hasn't come through, save the data and try to read
            # again
            if len(left_over) < size:
                self.left_over_tcp_data = left_over
                break

            # get the next message
            next_msg = left_over[:size]

            # shift our data pointer down
            data = left_over[size:]

            next_msg = json.loads(next_msg)

            # handle the new message
            self.on_read(s, next_msg)

    def send(self, s, msg):

        if isinstance(msg, dict):
            msg = json.dumps(msg)

        if isinstance(msg, str):
            msg = msg.encode()

        length = f"{len(msg)}@".encode()
        msg = length + msg

        try:
            s.send(msg)
        except:
            self.handle_exceptional(s)
