import pygame_gui
from engine.networkgameclient import NetworkGameClient
from engine.services.inputservice import InputService
import uuid
from pgu import text
import pygame


def create():
    # return UWUDP4Client(host="127.0.0.1")
    return UWUDP4Client()


class UWUDP4Client(NetworkGameClient):
    def __init__(self):
        super().__init__(width=680, height=440)
        self.font = pygame.font.SysFont("default", 24)
        self.player_1_score = 0
        self.player_2_score = 0
        self.score_text = None
        self.score_text_id = "#score_text_box"

    def on_read(self, s, message):
        super().on_read(s, message)

        type = message["type"]
        if type == "state":
            data = message["data"]
            self.player_1_score = data[0]
            self.player_2_score = data[1]

    def on_ui(self, dt):
        score_text = f"Player 1: {self.player_1_score}\nPlayer 2: {self.player_2_score}"

        if self.score_text is None:
            self.score_text = pygame_gui.elements.UITextBox(
                score_text,
                pygame.Rect(475, 15, 200, 100),
                self.game_service.ui_manager,
                object_id=self.score_text_id,
            )

        self.score_text.html_text = score_text
        self.score_text.rebuild()
        super().on_ui(dt)

    def on_load(self, game_service):
        super().on_load(game_service)

        game_service.input_service.register_mouse_motion(self.on_mouse_motion)
        game_service.input_service.register_mouse_click(self.on_mouse_click)
