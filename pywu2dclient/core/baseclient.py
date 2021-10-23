import pygame


class BaseClient:
    def __init__(self, width, height, should_render=True):
        self.tick_rate = 60
        self.exit = False
        self.width = width
        self.height = height

    def on_load(self, game_service):
        self.game_service = game_service
        self.game_service.event_manager.register_event(pygame.QUIT, self.on_quit)

    def on_close(self, game_service):
        pass

    def on_quit(self, event):
        self.on_close(self.game_service)
        pygame.quit()
        self.exit = True

    def process(self):
        raise NotImplementedError("Clients must implement process")

    def on_ui(self, dt):
        return

    def on_tick(self, dt):

        if self.exit:
            return

        self.game_service.event_manager.update()

        try:
            pygame.event.pump()
        except Exception:
            return

        self.pre_render()

        self.process(dt)

        self.on_ui(dt)

        self.render()
        self.post_render()

    def pre_render(self):
        pygame.display.get_surface().fill((0, 0, 0))

    def render(self):
        return

    def post_render(self):
        pygame.display.flip()
