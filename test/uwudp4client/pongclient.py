from engine.networkgameclient import NetworkGameClient
from engine.services.inputservice import InputService
import uuid
from pgu import text
import pygame


def create():
    return UWUDP4Client(host="127.0.0.1")
    # return UWUDP4Client(host="76.200.210.99")


class UWUDP4Client(NetworkGameClient):
    def __init__(self, host):
        super().__init__(host=host, port=41234, width=680, height=440)
        self.scores = {}
        self.font = pygame.font.SysFont("default", 24)

    def on_read(self, s, message):
        super().on_read(s, message)

        message["state"] = {"score": {"john": 0, "clay": "infinity"}}
        if "state" in message:
            state = message["state"]

            if "score" in state:
                score = state["score"]

                for k, v in score.items():
                    self.scores[k] = v
                score_text = "\n".join(f"{k}:{v}" for k, v in self.scores.items())

                text.writepre(
                    self.game_service.screen,
                    self.font,
                    pygame.Rect(0, 0, 200, 100),
                    "red",
                    score_text,
                )

    def on_load(self, game_service):
        super().on_load(game_service)

        game_service.input_service.register_mouse_motion(self.on_mouse_motion)

    def on_mouse_motion(self, x, y):
        self.send_message("game", {"type": "mouse", "x": x, "y": y})
