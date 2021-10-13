########################################################################################################################
#
########################################################################################################################
import argparse
import sys

from engine.gameclient import GameClient
from engine.gameservice import GameService
from engine.event.eventmanager import EventManager
import sys
import importlib.util

from timeit import default_timer as timer

import pygame

########################################################################################################################
#
########################################################################################################################
def run(game: GameClient):
    pygame.init()
    screen = pygame.display.set_mode((game.width, game.height))
    clock = pygame.time.Clock()
    event_manager = EventManager()
    game_service = GameService(event_manager=event_manager)

    game.on_load(game_service=game_service)

    tick_period = 1.0 / float(game.tick_rate)

    last_tick = timer()
    while not game.exit:
        now = timer()
        if (now - last_tick) >= tick_period:
            last_tick = now
            event_manager.update()
            game.on_tick(now - last_tick)

########################################################################################################################
#
########################################################################################################################
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--game-package', dest='game_package',  help='Path to the game module to load')

    args = parser.parse_args(sys.argv[1:])

    spec = importlib.util.spec_from_file_location("game_package", args.game_package)
    game_package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_package)
    game = game_package.create()
    run(game)


########################################################################################################################
#
########################################################################################################################
if __name__ == '__main__':
    main()