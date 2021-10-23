import pygame
from timeit import default_timer as timer
import time

from .core.pywu2dclient import PyWU2DClient
from .core.event.eventmanager import EventManager
from .core.gameservice import GameService


__all__ = [
    "PyWU2DClient",
    "EventManager",
    "GameService",
]

CLIENT_TICK_RATE = 60


def main_loop(game_factory):

    pygame.init()
    pygame.font.init()

    game = game_factory()

    screen_size = (game.width, game.height)
    screen = pygame.display.set_mode(screen_size)
    event_manager = EventManager()
    game_service = GameService(screen_size, screen=screen, event_manager=event_manager)

    game.on_load(game_service=game_service)

    period = 1 / CLIENT_TICK_RATE

    last_tick = timer()
    while not game.exit:
        now = timer()
        game.on_tick(now - last_tick)
        end = timer()

        last_tick = end
        time.sleep(period - (end - now))
