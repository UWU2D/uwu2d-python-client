import uuid
from engine.network.udp.udpclient import UDPClient
from engine.services.inputservice import InputService
from engine.sprite.polygonsprite2d import PolygonSprite2D

from engine.sprite.circlesprite import CircleSprite
from engine.network.udp.udpclient import UDPClient
from engine.gameclient import GameClient

from timeit import default_timer as timer


class NetworkGameClient(GameClient):
    def __init__(self, host, port, *args, **kwargs):
        GameClient.__init__(self, *args, **kwargs)

        self.join_id = str(uuid.uuid4())

        self.client_id = None

        self.last_handshake_time = timer()
        self.try_to_handshake_period_ms = 1000

        self.last_heartbeat_request_time = timer()
        self.heartbeat_timeout_ms = 2000

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

    def on_load(self, game_service):
        super().on_load(game_service)

    def on_connect(self, s):
        self.last_heartbeat_request_time = timer()

    def on_disconnect(self):
        pass

    def on_close(self, game_service):
        super().on_close(game_service)
        # self.tcp_client.stop()
        self.udp_client.stop()

    def on_read(self, s, message):

        type = message["type"]
        data = message["data"]

        if type == "handshake":
            print("Handshake")
            if self.client_id is None:
                self.client_id = data["id"]
                self.should_handshake = False
                self.on_connect(s)
            else:
                print("Got second client id")
        elif type == "game":
            self.sync_entities(data)
        elif type == "heartbeat":
            print("heartbeat")
            self.send_hearbeat()
        elif type == "state":
            pass
        else:
            print(f"Unknown message type {type}")

    def sync_entities(self, game_objects):

        for game_object in game_objects:
            self.sync_entity(game_object)

    def sync_entity(self, game_object):
        id = game_object["id"]
        type = game_object["type"]

        # we have not encountered this sprite yet
        if id not in self.sprites:
            print(game_object)
            # create it based on the types we know
            if type == "circle":
                self.sprites[id] = CircleSprite(id=id)
            elif type == "polygon":
                self.sprites[id] = PolygonSprite2D(id=id)
            else:
                print("Unknown sprite type: " + type)
                return

        # Update the info
        self.sprites[id].from_sync_info(game_object)

    def on_tick(self, dt):
        super().on_tick(dt=dt)

        if self.connection_severed() and self.client_id is not None:
            self.on_disconnect()
            self.destroy_all_entities()
            self.client_id = None

        if self.should_send_handshake():
            self.send_handshake()

        self.process_network()

    def process_network(self):
        # self.tcp_client.process()
        self.udp_client.process()

    def should_send_handshake(self):
        if self.client_id is not None:
            return False

        return (timer() - self.last_handshake_time) * 1000 > self.try_to_handshake_period_ms

    def connection_severed(self):
        return (timer() - self.last_heartbeat_request_time) * 1000 > self.heartbeat_timeout_ms

    def send_hearbeat(self):
        self.send_message("heartbeat", {})
        self.last_heartbeat_request_time = timer()

    def send_handshake(self):
        self.send_message("handshake", {})
        self.last_handshake_time = timer()

    def send_message(self, type, data, guarantee=False):
        transport = self.udp_client
        if guarantee:
            transport = self.udp_client

        transport.send_message({
            "type": type,
            "messageId": str(uuid.uuid4()),
            "clientId": self.client_id,
            "data": data
        })
