from engine.networkgameclient import NetworkGameClient
from engine.services.inputservice import InputService
import uuid


def create():
    return UWUDP4Client(host="127.0.0.1")


class UWUDP4Client(NetworkGameClient):
    def __init__(self, host):
        super().__init__(host=host, port=41234, width=680, height=420)

    def on_read(self, s, message):
        super().on_read(s, message)

    def on_load(self, game_service):
        super().on_load(game_service)

        # register for input
        game_service.input_service.register_key_event(
            InputService.KEY_UP, self.on_up_arrow
        )
        game_service.input_service.register_key_event(
            InputService.KEY_DOWN, self.on_down_arrow
        )
        game_service.input_service.register_key_event(
            InputService.KEY_LEFT, self.on_left_arrow
        )
        game_service.input_service.register_key_event(
            InputService.KEY_RIGHT, self.on_right_arrow
        )
        game_service.input_service.register_mouse_motion(self.on_mouse_motion)

    def on_up_arrow(self, key, pressed):
        self.on_arrow("up", pressed)

    def on_down_arrow(self, key, pressed):
        self.on_arrow("down", pressed)

    def on_left_arrow(self, key, pressed):
        self.on_arrow("left", pressed)

    def on_right_arrow(self, key, pressed):
        self.on_arrow("right", pressed)

    def on_arrow(self, key_name, pressed):
        self.udp_client.send_message(
            {
                "type": "game",
                "messageId": str(uuid.uuid4()),
                "clientId": self.client_id,
                "data": {"type": "keyPress", "key": key_name, "pressed": pressed},
            }
        )

        self.next_id += 1

    def on_mouse_motion(self, x, y):
        self.udp_client.send_message(
            {
                "type": "game",
                "messageId": str(uuid.uuid4()),
                "clientId": self.client_id,
                "data": {"type": "mouse", "x": x, "y": y},
            }
        )
        self.next_id += 1
