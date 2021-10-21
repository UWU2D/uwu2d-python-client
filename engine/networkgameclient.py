import uuid
import pygame

import pygame_gui
from engine.network.udp.udpclient import UDPClient
from engine.services.inputservice import InputService
from engine.services.timer import Timer
from engine.sprite.polygonsprite2d import PolygonSprite2D

from engine.sprite.circlesprite import CircleSprite
from engine.network.udp.udpclient import UDPClient
from engine.gameclient import GameClient

from engine.network.ws.wsclient import WSClient


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
        # self.udp_client: UDPClient = UDPClient(
        #     server_ip=host, server_port=port, self_port=port
        # )
        # self.udp_client.on_read = self.on_read

        # self.ws_client = WSClient(host, port)
        # self.ws_client.on_connect = self.on_connect
        # self.ws_client.on_disconnect = self.on_disconnect
        # self.ws_client.on_read = self.on_read
        # self.use_udp = False

        self.message_processing = {
            "handshake": self.on_handshake,
            "game": self.on_game,
            "heartbeat": self.on_heartbeat,
            "state": self.on_state,
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
        self.udp_client.stop()
        self.ws_client.stop()

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

    def on_ui(self, dt):

        if self.wait_for_user_input:
            if self.server_window is None:
                self.server_window = pygame_gui.elements.UIWindow(
                    pygame.Rect(0, 0, 400, 300), self.game_service.ui_manager
                )

                self.server_ip = pygame_gui.elements.UITextEntryLine(
                    pygame.Rect(25, 25, 100, 300),
                    self.game_service.ui_manager,
                    self.server_window,
                )
                self.server_port = pygame_gui.elements.UITextEntryLine(
                    pygame.Rect(25, 50, 100, 300),
                    self.game_service.ui_manager,
                    self.server_window,
                )
                self.connect_button = pygame_gui.elements.UIButton(
                    pygame.Rect(100, 200, 100, 300),
                    text="Click",
                    manager=self.game_service.ui_manager,
                    container=self.server_window,
                )

                self.game_service.event_manager.register_event(
                    pygame.USEREVENT, self.on_server_data_entry
                )
                # self.server_window.add(
                #     [
                #         pygame_gui.elements.UIButton(
                #             pygame.Rect(0, 0, 50, 50),
                #             "Click Me",
                #             self.game_service.ui_manager,
                #         )
                #     ]
                # )
        super().on_ui(dt)

    def on_server_data_entry(self, event):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.connect_button:
                self.try_connect(self.server_ip.text, self.server_port.text)

    def try_connect(self, host, port):
        if self.ws_client is None:
            self.ws_client = WSClient(host, port)
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
        # self.tcp_client.process()
        pass

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
