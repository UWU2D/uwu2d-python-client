import uuid
from engine.gameclient import GameClient

from engine.network.ws.wsclient import WSClient
from engine.services.timer import Timer


class NetworkGameClient(GameClient):
    def __init__(self, width, height, *args, **kwargs):
        GameClient.__init__(self, width, height, *args, **kwargs)

        self.join_id = str(uuid.uuid4())

        self.client_id = None

        self.handshake_timer = Timer(1000)
        self.heartbeat_timer = Timer(2000)

        self.wait_for_user_input = True

        self.ws_client = None
        self.udp_client = None

        self.message_processing = {
            "handshake": self.on_handshake,
            "heartbeat": self.on_heartbeat,
        }

        self.server_window = None

    def on_load(self, game_service):
        super().on_load(game_service)

    def on_connect(self, s):
        self.connected = True
        self.heartbeat_timer.reset()
        self.server_window.kill()

    def on_disconnect(self):
        self.destroy_all_entities()
        self.client_id = None
        self.connected = False
        self.server_window.show()

    def on_close(self, game_service):
        super().on_close(game_service)
        # self.tcp_client.stop()
        if self.udp_client:
            self.udp_client.stop()
        if self.ws_client:
            self.ws_client.stop()

    def on_read(self, socket, message):

        type = message["type"]

        if type in self.message_processing:
            self.message_processing[type](socket, message["data"])

    def on_handshake(self, socket, data):
        if self.client_id is None:
            self.client_id = data["id"]
            self.should_handshake = False
            self.on_connect(socket)
        else:
            print("Got second client id")

    def on_heartbeat(self, socket, data):
        self.send_hearbeat()

    def on_state(self, socket, data):
        return

    def try_connect(self, url):
        if self.ws_client is None:
            self.ws_client = WSClient(url)
            self.ws_client.on_connect = self.on_connect
            self.ws_client.on_disconnect = self.on_disconnect
            self.ws_client.on_read = self.on_read
            self.use_udp = False
            self.wait_for_user_input = False

    def process(self, dt):

        self.process_network()

        if self.wait_for_user_input:
            return

        if self.use_udp and self.connection_severed() and self.client_id is not None:
            self.on_disconnect()

        if self.should_send_handshake():
            self.send_handshake()

    def process_network(self):
        if self.udp_client is not None:
            self.udp_client.process()
        if self.ws_client is not None:
            self.ws_client.process()

    def should_send_handshake(self):
        if self.client_id is not None:
            return False

        return self.handshake_timer.is_elapsed()

    def connection_severed(self):
        return self.heartbeat_timer.is_elapsed()

    def send_hearbeat(self):
        self.send_message("heartbeat", {})
        self.heartbeat_timer.reset()

    def send_handshake(self):
        self.send_message("handshake", {})
        self.handshake_timer.reset()

    def send_message(self, type, data, guarantee=False):

        if self.wait_for_user_input:
            return

        if self.use_udp:
            transport = self.udp_client
        else:
            transport = self.ws_client

        transport.send(
            {
                "type": type,
                "messageId": str(uuid.uuid4()),
                "clientId": self.client_id,
                "data": data,
            }
        )
