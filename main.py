import argparse
import sys

from engine.gameclient import GameClient
from engine.gameservice import GameService
from engine.event.eventmanager import EventManager
import sys
import importlib.util

from timeit import default_timer as timer

import pygame


def run(game: GameClient):
    pygame.init()
    screen = pygame.display.set_mode((game.width, game.height))
    event_manager = EventManager()
    game_service = GameService(event_manager=event_manager)

    game.on_load(game_service=game_service)

    last_tick = timer()
    while not game.exit:
        now = timer()
        event_manager.update()
        game.on_tick(now - last_tick)
        last_tick = now


########################################################################################################################
#
########################################################################################################################
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--game-package", dest="game_package", help="Path to the game module to load"
    )

    args = parser.parse_args(sys.argv[1:])

    spec = importlib.util.spec_from_file_location(
        "game_package", args.game_package)
    game_package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_package)
    game = game_package.create()
    run(game)


########################################################################################################################
#
########################################################################################################################
if __name__ == "__main__":
    main()
