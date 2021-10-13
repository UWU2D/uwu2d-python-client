import pygame
from engine.services.inputservice import InputService


class GameService:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.input_service = InputService()

        # pip key events to input service
        event_manager.register_event(pygame.KEYDOWN, self.input_service.on_event)
        event_manager.register_event(pygame.KEYUP, self.input_service.on_event)
        event_manager.register_event(pygame.MOUSEMOTION, self.input_service.on_event)
        event_manager.register_event(pygame.MOUSEBUTTONUP, self.input_service.on_event)
        event_manager.register_event(
            pygame.MOUSEBUTTONDOWN, self.input_service.on_event
        )
