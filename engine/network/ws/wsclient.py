import websocket
import json
import threading
import queue


class WSClient:
    def __init__(self, host=None, port=None):
        self.url = f"ws://{host}:{port}"
        self.socket = websocket.WebSocket()

        self.run_thread = True
        self.read_queue = queue.Queue()
        self.thread = None

    def is_connected(self):
        return self.socket.connected

    def stop(self):
        self.run_thread = False
        self.thread.join()

    def on_connect(self, s):
        raise NotImplementedError("Implement on_connect")

    def on_disconnect(self, s):
        raise NotImplementedError("Implement on_disconnect")

    def on_read(self, s, msg):
        raise NotImplementedError("Implement on_read")

    def read_thread(self):
        while self.run_thread:
            try:
                msg = self.socket.recv()
            except Exception as e:
                continue
            else:
                self.read_queue.put(msg)

    def process(self):
        if not self.socket.connected:
            self.connect()

            if not self.socket.connected:
                return
            else:
                self.thread = threading.Thread(target=self.read_thread)
                self.thread.start()

        while not self.read_queue.empty():
            next = self.read_queue.get_nowait()
            try:
                msg = json.loads(next)
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
