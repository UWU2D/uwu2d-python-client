import pygame
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
        game_service.input_service.register_mouse_click(self.on_mouse_click)

    def on_up_arrow(self, key, pressed):
        self.on_arrow("up", pressed)

    def on_down_arrow(self, key, pressed):
        self.on_arrow("down", pressed)

    def on_left_arrow(self, key, pressed):
        self.on_arrow("left", pressed)

    def on_right_arrow(self, key, pressed):
        self.on_arrow("right", pressed)

    def on_arrow(self, key_name, pressed):
        self.send_message(
            "game", {"type": "keyPress", "key": key_name, "pressed": pressed}
        )

    def on_mouse_motion(self, x, y):
        self.send_message("game", {"type": "mouse", "x": x, "y": y})

    def on_mouse_click(self, x, y, button, pressed):
        if button == pygame.BUTTON_LEFT:
            self.send_message("game", {"type": "click", "x": x, "y": y, "pressed": pressed})
