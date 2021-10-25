import uuid
import json

from .timer import Timer


class UWU2DService:
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

        self.__maintain_network()

        if self.network_client.is_connected():
            self.__read_network()

        if self.__should_send_handshake():
            self.__send_handshake()

    def stop(self):
        self.network_client.stop()

    def send_message(self, type, data):
        self.network_client.send(
            {
                "type": type,
                "messageId": str(uuid.uuid4()),
                "clientId": self.client_id,
                "data": data,
            }
        )

    def __maintain_network(self):
        # nothing to do if client is connected
        if self.network_client.is_connected():
            if not self.was_previously_connected:
                self.__handle_connect()

            return

        # on previous loop, we were connected, so we just caught a disconnect
        if self.was_previously_connected:
            self.__handle_disconnect()
        # previous loop was not connected, try to connect
        else:
            self.network_client.connect()

    def __read_network(self):
        try:
            messages = self.network_client.read()
        except Exception as e:
            return
        else:
            for message in messages:
                self.__handle_message(message)

    def __handle_disconnect(self):
        self.was_previously_connected = False
        self.handshake_timer.reset()
        self.message_handler.on_disconnect()

    def __handle_connect(self):
        self.was_previously_connected = True
        self.__send_sync()
        self.message_handler.on_connect()

    def __handle_message(self, message):
        message = json.loads(message)

        message_type = message["type"]
        message_id = message["messageId"]
        data = message["data"]

        if message_type == "handshake":
            self.__handle_handshake(data)
            if "config" in data:
                self.message_handler.on_client_config(data["config"])
        elif message_type == "sync":
            self.__handle_sync(data)
        else:
            self.message_handler.on_read(message_type, message_id, data)

    def __handle_handshake(self, message):
        self.client_id = message["id"]
        self.message_handler.on_handshake(self.client_id)

    def __handle_sync(self, message):
        self.message_handler.on_sync(message)

    def __should_send_handshake(self):
        if self.client_id is not None:
            return False

        return self.handshake_timer.is_elapsed()

    def __send_handshake(self):
        self.send_message("handshake", {})
        self.handshake_timer.reset()

    def __send_sync(self):
        self.send_message("sync", {})
