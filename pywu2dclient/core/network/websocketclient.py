import websocket
import json
import threading
import queue

from ...public.networkclient import INetworkClient


class WebsocketClient(INetworkClient):
    def __init__(self, url=None):

        self.url = url
        self.socket = websocket.WebSocket()

        self.run_thread = True
        self.read_queue = queue.Queue()
        self.thread = None
        self.previously_connected = False

    def is_connected(self):
        return self.socket.connected

    def connect(self):
        if self.socket.connected:
            return True

        try:
            self.socket.connect(self.url)
        except Exception as e:
            # print(str(e))
            return False

        self.previously_connected = True
        if self.thread is None:
            self.thread = threading.Thread(target=self.read_thread)
            self.thread.start()

        return True

    def stop(self):
        self.run_thread = False
        if self.thread is not None:
            self.thread.join()
        return True

    def read(self):
        messages = []
        while not self.read_queue.empty():
            messages.append(self.read_queue.get_nowait())

        return messages

    def send(self, msg):
        try:
            self.socket.send(json.dumps(msg))
        except Exception as e:
            return False

        return True

    def read_thread(self):
        while self.run_thread:
            if not self.socket.connected:
                continue

            try:
                msg = self.socket.recv()
            except ConnectionResetError as e:
                self.socket.close()
            except websocket.WebSocketConnectionClosedException as e:
                self.socket.close()
            else:
                self.read_queue.put(msg)

    # def process(self):
    #     if not self.socket.connected:
    #         if self.previously_connected:
    #             self.on_disconnect()
    #             self.previously_connected = False
    #         else:
    #             self.connect()

    #             if not self.socket.connected:
    #                 return
    #             else:
    #                 if self.thread is None:
    #                     self.thread = threading.Thread(target=self.read_thread)
    #                     self.thread.start()

    #     while not self.read_queue.empty():
    #         next = self.read_queue.get_nowait()
    #         try:
    #             msg = json.loads(next)
    #         except Exception as e:
    #             print("Error converting messsage to json: " + str(e))
    #             return

    #         if msg not in [None, ""]:
    #             self.on_read(self.socket, msg)
