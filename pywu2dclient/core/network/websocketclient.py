from socket import socket
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
        self.try_to_connect = True

        self.read_queue = queue.Queue()
        self.thread = threading.Thread(target=self.thread_read)
        self.thread.start()

    def is_connected(self):
        return self.socket.connected

    def connect(self):
        if self.socket.connected:
            return True

        self.try_to_connect = True
        return False

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

    def thread_read(self):
        while self.run_thread:

            if not self.socket.connected and self.try_to_connect:
                self.thread_connect()

            if not self.socket.connected:
                continue

            if self.try_to_connect:
                self.try_to_connect = False

            try:
                msg = self.socket.recv()
            except ConnectionResetError as e:
                self.socket.close()
            except websocket.WebSocketConnectionClosedException as e:
                self.socket.close()
            else:
                self.read_queue.put(msg)

    def thread_connect(self):
        try:
            self.socket.connect(self.url)
        except Exception as e:
            pass
