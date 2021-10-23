import pygame
from timeit import default_timer as timer

from .core.pywu2dclient import PyWU2DClient
from .core.event.eventmanager import EventManager
from .core.gameservice import GameService
from .core import sprite
from .core import services
from .core import network
from .core import math
from .core import drawable
from .core import event


__all__ = [
    "PyWU2DClient",
    "EventManager",
    "GameService",
]


def main_loop(game_factory):

    pygame.init()
    pygame.font.init()

    game = game_factory()

    screen_size = (game.width, game.height)
    screen = pygame.display.set_mode(screen_size)
    event_manager = EventManager()
    game_service = GameService(screen_size, screen=screen, event_manager=event_manager)

    game.on_load(game_service=game_service)

    last_tick = timer()
    while not game.exit:
        now = timer()
        game.on_tick(now - last_tick)
        last_tick = now
