import uuid
from engine.network.udp.udpclient import UDPClient
from engine.services.inputservice import InputService
from engine.sprite.polygonsprite2d import PolygonSprite2D

from engine.sprite.circlesprite import CircleSprite
from engine.network.udp.udpclient import UDPClient
from engine.gameclient import GameClient


class NetworkGameClient(GameClient):
    def __init__(self, host, port, *args, **kwargs):
        GameClient.__init__(self, *args, **kwargs)

        self.join_id = str(uuid.uuid4())
        self.client_id = None

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

        self.udp_client.send_message({"type": "internal", "messageId": self.join_id})

    def on_connect(self, s):
        pass

    def on_disconnect(self, s):
        pass

    def on_close(self, game_service):
        super().on_close(game_service)
        # self.tcp_client.stop()
        self.udp_client.stop()

    def on_read(self, s, data):

        typekey = data["type"]
        data = data["data"]

        if typekey == "internal":
            self.client_id = data["id"]
        elif typekey == "game":
            self.sync_entities(data)

    def sync_entities(self, game_objects):

        for game_object in game_objects:

            id = game_object["id"]
            type = game_object["type"]

            # we have not encountered this sprite yet
            if id not in self.sprites:
                # create it based on the types we know
                if type == "circle":
                    self.sprites[id] = CircleSprite(id=id)
                elif type == "polygon":
                    self.sprites[id] = PolygonSprite2D(id=id)
                else:
                    print("Unknown sprite type: " + type)
                    continue

            # Update the info
            self.sprites[id].from_sync_info(game_object)

    def destroy_entities(self, ids):
        for id in ids:
            if id in self.sprites:
                self.destroy(self.sprites[id])
            else:
                print("Cannot destroy " + str(id) + " it doesn't exist")

    def on_tick(self, dt):
        super().on_tick(dt=dt)

        # self.tcp_client.process()
        self.udp_client.process()
