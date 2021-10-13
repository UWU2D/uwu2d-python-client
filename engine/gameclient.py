import pygame


class GameClient:
    def __init__(self, should_render=True):
        self.tick_rate = 60
        self.exit = False
        self.width = 680
        self.height = 420

        self.next_id = 0

        self.should_render = should_render

        self.sprites = {}
        self.collisions = []

    def on_load(self, game_service):
        self.game_service = game_service

        self.game_service.event_manager.register_event(pygame.QUIT, self.on_quit)

    def on_close(self, game_service):
        pass

    def on_quit(self, event):
        self.on_close(self.game_service)
        pygame.quit()
        self.exit = True

    def on_tick(self, dt):

        if self.exit:
            return

        pygame.event.pump()

        for sprite in self.sprites.values():
            sprite.tick(dt)

        for structure in self.collisions:
            root, other, callback = structure
            if root.collides(other):
                callback(root, other)

        if self.should_render:
            pygame.display.get_surface().fill((0, 0, 0))

            for sprite in self.sprites.values():
                if sprite.drawable is not None:
                    sprite.drawable.draw(pygame.display.get_surface(), sprite)

            pygame.display.flip()

    def instantiate(self, type, debug_name, *args, **kwargs):

        id = self.next_id
        self.next_id += 1
        self.sprites[id] = type(id, debug_name=debug_name, *args, **kwargs)

        return self.sprites[id]

    def destroy(self, object):
        if object is None:
            return

        if object.id in self.sprites:
            del self.sprites[object.id]

        if object in self.collisions:
            del self.collisions[object]

        # trim any collisions that have a root of the thing we just removed
        self.collisions[:] = [
            x for x in self.collisions if x[0] is not object and x[1] is not object
        ]

    def enable_collision(
        self,
        root,
        other,
        on_collision,
    ):
        if root.collider is None or other.collider is None:
            return

        self.collisions.append((root, other, on_collision))
