import pygame
from .services.inputservice import InputService


class GameService:
    def __init__(self, screen_size, screen, event_manager):
        self.event_manager = event_manager
        self.input_service = InputService()
        self.screen = screen
        self.screen_size = screen_size

        # pip key events to input service
        event_manager.register_event(pygame.KEYDOWN, self.input_service.on_event)
        event_manager.register_event(pygame.KEYUP, self.input_service.on_event)
        event_manager.register_event(pygame.MOUSEMOTION, self.input_service.on_event)
        event_manager.register_event(pygame.MOUSEBUTTONUP, self.input_service.on_event)
        event_manager.register_event(
            pygame.MOUSEBUTTONDOWN, self.input_service.on_event
        )
