from engine.networkgameclient import NetworkGameClient
from engine.services.inputservice import InputService
import uuid
from pgu import text
import pygame


def create():
    # return UWUDP4Client(host="127.0.0.1")
    return UWUDP4Client(host="76.200.210.99")


class UWUDP4Client(NetworkGameClient):
    def __init__(self, host):
        super().__init__(host=host, port=41234, width=680, height=440)
        self.font = pygame.font.SysFont("default", 24)
        self.player_1_score = 0
        self.player_2_score = 0

    def on_read(self, s, message):
        super().on_read(s, message)

        type = message["type"]
        if type == "state":
            data = message["data"]
            self.player_1_score = data[0]
            self.player_2_score = data[1]

    def on_ui(self):
        score_text = f"Player 1: {self.player_1_score}\nPlayer 2: {self.player_2_score}"
        text.writepre(
            self.game_service.screen,
            self.font,
            pygame.Rect(575, 15, 200, 100),
            "red",
            score_text,
        )

    def on_load(self, game_service):
        super().on_load(game_service)

        game_service.input_service.register_mouse_motion(self.on_mouse_motion)

    def on_mouse_motion(self, x, y):
        self.send_message("game", {"type": "mouse", "x": x, "y": y})
