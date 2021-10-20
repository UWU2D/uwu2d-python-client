import websocket
import json


class WSClient:
    def __init__(self, host=None, port=None):
        self.url = f"ws://{host}:{port}"
        self.socket = websocket.WebSocket()

    def is_connected(self):
        return self.socket.connected

    def on_connect(self, s):
        raise NotImplementedError("Implement on_connect")

    def on_disconnect(self, s):
        raise NotImplementedError("Implement on_disconnect")

    def on_read(self, s, msg):
        raise NotImplementedError("Implement on_read")

    def process(self):
        if not self.socket.connected:
            self.connect()

            if not self.socket.connected:
                return

        try:
            msg = self.socket.recv()
        except Exception as e:
            return

        try:
            msg = json.loads(msg)
        except Exception as e:
            print("Error converting messsage to json: " + str(e))
            return

        if msg not in [None, ""]:
            self.on_read(self.socket, msg)

    def send(self, msg):
        try:
            self.socket.send(json.dumps(msg))
        except Exception as e:
            return

    def connect(self):
        if self.socket.connected:
            return

        try:
            self.socket.connect(self.url)
        except Exception as e:
            # print(str(e))
            return

        self.on_connect(self.socket)
