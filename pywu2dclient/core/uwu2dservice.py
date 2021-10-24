import uuid
import json

from .timer import Timer

from ..public.uwu2dservice import IUWU2DService


class UWU2DService(IUWU2DService):
    def __init__(self, network_client, message_handler):
        self.network_client = network_client
        self.message_handler = message_handler

        self.was_previously_connected = False

        self.client_id = None
        self.join_id = str(uuid.uuid4())

        self.handshake_timer = Timer(1000)

    def is_connected(self):
        if self.network_client is None:
            return False

        return self.network_client.is_connected()

    def maintain(self):

        self.maintain_network()

        if self.network_client.is_connected():
            self.read_network()

        if self.should_send_handshake():
            self.handshake()

    def stop(self):
        self.network_client.stop()

    def maintain_network(self):
        # nothing to do if client is connected
        if self.network_client.is_connected():
            return

        # on previous loop, we were connected, so we just caught a disconnect
        if self.was_previously_connected:
            self.handle_disconnect()
        # previous loop was not connected, try to connect
        else:

            self.network_client.connect()

            # we are not connected
            if self.network_client.is_connected():
                self.handle_connect()

    def read_network(self):
        try:
            messages = self.network_client.read()
        except Exception as e:
            return
        else:
            for message in messages:
                self.handle_message(message)

    def handle_disconnect(self):
        self.was_previously_connected = False
        self.handshake_timer.reset()
        self.message_handler.on_disconnect()

    def handle_connect(self):
        self.was_previously_connected = True
        self.message_handler.on_connect()

    def handle_message(self, message):
        message = json.loads(message)

        message_type = message["type"]
        message_id = message["messageId"]
        data = message["data"]

        if message_type == "handshake":
            self.handle_handshake(data)
            if "config" in data:
                self.message_handler.on_client_config(data["config"])
        else:
            self.message_handler.on_read(message_type, message_id, data)

    def handle_handshake(self, message):
        self.client_id = message["id"]
        self.message_handler.on_handshake(self.client_id)

    def should_send_handshake(self):
        if self.client_id is not None:
            return False

        return self.handshake_timer.is_elapsed()

    def handshake(self):
        self.send_message("handshake", {})
        self.handshake_timer.reset()

    def send_message(self, type, data):
        self.network_client.send(
            {
                "type": type,
                "messageId": str(uuid.uuid4()),
                "clientId": self.client_id,
                "data": data,
            }
        )
