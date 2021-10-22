from engine.networkgameclient import NetworkGameClient
from engine.services.inputservice import InputService
import uuid


def create():
    return UWUDP4Client(host="127.0.0.1")
    # return UWUDP4Client(host="76.200.210.99")


class UWUDP4Client(NetworkGameClient):
    def __init__(self, host):
        super().__init__(width=1920, height=1280)

    def on_read(self, s, message):
        super().on_read(s, message)

    def on_load(self, game_service):
        super().on_load(game_service)

        # register for input
        self.register_key(InputService.KEY_UP)
        self.register_key(InputService.KEY_DOWN)
        self.register_key(InputService.KEY_LEFT)
        self.register_key(InputService.KEY_RIGHT)

        game_service.input_service.register_mouse_motion(self.on_mouse_motion)
        game_service.input_service.register_mouse_click(self.on_mouse_click)

    def on_mouse_motion(self, x, y):
        self.send_message("game", {"type": "mouse", "x": x, "y": y})

    def on_mouse_click(self, x, y, left, right):
        print(f"{x}:{y}:{left}:{right}")
