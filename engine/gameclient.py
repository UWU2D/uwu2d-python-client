import pygame


class GameClient:
    def __init__(self, width, height, should_render=True):
        self.tick_rate = 60
        self.exit = False
        self.width = width
        self.height = height

        self.next_id = 0

        self.should_render = should_render

        self.sprites = {}

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
        self.game_service.ui_manager.update(dt)

    def on_tick(self, dt):

        if self.exit:
            return

        self.game_service.event_manager.update()

        try:
            pygame.event.pump()
        except Exception:
            return

        if self.should_render:
            self.pre_render()

        self.process(dt)

        for sprite in self.sprites.values():
            sprite.tick(dt)

        self.on_ui(dt)

        self.game_service.ui_manager.draw_ui(self.game_service.screen)

        if self.should_render:
            self.render()
            self.post_render()

    def pre_render(self):
        pygame.display.get_surface().fill((0, 0, 0))

    def render(self):
        for sprite in self.sprites.values():
            if sprite.drawable is not None:
                sprite.drawable.draw(pygame.display.get_surface(), sprite)

    def post_render(self):
        pygame.display.flip()

    def instantiate(self, type, debug_name, *args, **kwargs):

        id = self.next_id
        self.next_id += 1
        self.sprites[id] = type(id, debug_name=debug_name, *args, **kwargs)

        return self.sprites[id]

    def destroy_all_entities(self):
        print("Destroying entities")
        self.sprites.clear()

    def destroy(self, id):
        if id in self.sprites:
            del self.sprites[id]
