import pygame


class EventManager:
    def __init__(self):
        super().__init__()
        self.listeners = {}
        self.all_listeners = []

    def register_event(self, type, callback):
        if type not in self.listeners:
            self.listeners[type] = []

        self.listeners[type].append(callback)

    def register_for_all(self, callback):
        self.all_listeners.append(callback)

    def update(self):
        for event in pygame.event.get():
            if event.type in self.listeners:
                for c in self.listeners[event.type]:
                    c(event)
            for c in self.all_listeners:
                c(event)
