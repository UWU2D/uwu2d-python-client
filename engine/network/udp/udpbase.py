import socket
import json


class UDPBase:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)

    def process(self):
        pass

    def stop(self):
        self.socket.close()

    def on_read(self, s, data):
        raise NotImplementedError("Implement UDPBase.on_read")

    def read(self):
        while True:
            try:
                raw_buffer, sender = self.socket.recvfrom(8192)
            except socket.error as e:
                if e.errno != 10035:
                    pass
                    # print (str(e))
                return

            if raw_buffer in [None, b""]:
                return

            # put it in string form
            data = raw_buffer.decode()

            data = json.loads(data)

            self.on_read(sender, data)

    def send_to(self, host, port, data):

        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, str):
            data = data.encode()

        num_sent = self.socket.sendto(data, (host, port))
        i = 0
