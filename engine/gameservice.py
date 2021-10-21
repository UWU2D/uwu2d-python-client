import pygame
from engine.services.inputservice import InputService

import pygame_gui


class GameService:
    def __init__(self, screen_size, screen, event_manager):
        self.event_manager = event_manager
        self.input_service = InputService()
        self.screen = screen

        self.ui_manager = pygame_gui.UIManager(screen_size)
        self.ui_manager.get_sprite_group()

        # pip key events to input service
        event_manager.register_event(pygame.KEYDOWN, self.input_service.on_event)
        event_manager.register_event(pygame.KEYUP, self.input_service.on_event)
        event_manager.register_event(pygame.MOUSEMOTION, self.input_service.on_event)
        event_manager.register_event(pygame.MOUSEBUTTONUP, self.input_service.on_event)
        event_manager.register_event(
            pygame.MOUSEBUTTONDOWN, self.input_service.on_event
        )
        event_manager.register_for_all(self.pass_to_ui)

    def pass_to_ui(self, event):
        self.ui_manager.process_events(event)
