import uuid
from engine.network.udp.udpclient import UDPClient
from engine.services.inputservice import InputService
from engine.services.timer import Timer
from engine.sprite.polygonsprite2d import PolygonSprite2D

from engine.sprite.circlesprite import CircleSprite
from engine.network.udp.udpclient import UDPClient
from engine.gameclient import GameClient


class NetworkGameClient(GameClient):
    def __init__(self, host, port, width, height, *args, **kwargs):
        GameClient.__init__(self, width, height, *args, **kwargs)

        self.join_id = str(uuid.uuid4())

        self.client_id = None

        self.handshake_timer = Timer(10000)
        self.heartbeat_timer = Timer(2000)

        # monkey patch tcp client
        # self.tcp_client:TCPClient       = TCPClient(host=host, port=port)
        # self.tcp_client.on_connect      = self.on_connect
        # self.tcp_client.on_disconnect   = self.on_disconnect
        # self.tcp_client.on_read         = self.on_read

        # monkey patch udp client
        self.udp_client: UDPClient = UDPClient(
            server_ip=host, server_port=port, self_port=port
        )
        self.udp_client.on_read = self.on_read

        self.message_processing = {
            "handshake": self.on_handshake,
            "game": self.on_game,
            "heartbeat": self.on_heartbeat,
            "state": self.on_state,
        }

    def on_load(self, game_service):
        super().on_load(game_service)

    def on_connect(self, s):
        self.heartbeat_timer.reset()

    def on_disconnect(self):
        self.destroy_all_entities()
        self.client_id = None

    def on_close(self, game_service):
        super().on_close(game_service)
        # self.tcp_client.stop()
        self.udp_client.stop()

    def on_read(self, socket, message):

        type = message["type"]

        if type not in self.message_processing:
            print(f"Unknown message type {type}")

        self.message_processing[type](socket, message["data"])

    def on_handshake(self, socket, data):
        if self.client_id is None:
            self.client_id = data["id"]
            self.should_handshake = False
            self.on_connect(socket)
        else:
            print("Got second client id")

    def on_game(self, socket, data):
        self.sync_entities(data)

    def on_heartbeat(self, socket, data):
        self.send_hearbeat()

    def on_state(self, socket, data):
        return

    def on_tick(self, dt):
        super().on_tick(dt=dt)

        if self.connection_severed() and self.client_id is not None:
            self.on_disconnect()

        if self.should_send_handshake():
            self.send_handshake()

        self.process_network()

    def process_network(self):
        # self.tcp_client.process()
        self.udp_client.process()

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
        transport = self.udp_client
        if guarantee:
            transport = self.udp_client

        transport.send_message(
            {
                "type": type,
                "messageId": str(uuid.uuid4()),
                "clientId": self.client_id,
                "data": data,
            }
        )

    def sync_entities(self, game_objects):
        for game_object in game_objects:
            self.sync_entity(game_object)

    def sync_entity(self, game_object):
        id = game_object["id"]
        type = game_object["data"]["shape"]

        # we have not encountered this sprite yet
        if id not in self.sprites:
            # create it based on the types we know
            if type == "circle":
                self.sprites[id] = CircleSprite(id=id)
            elif type == "polygon":
                self.sprites[id] = PolygonSprite2D(id=id)
            else:
                print("Unknown sprite type: " + type)
                return

        if game_object["state"] == "deleted":
            self.destroy(id)
        else:
            # Update the info
            self.sprites[id].sync(game_object)
