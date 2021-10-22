from ..drawable.circledrawable import CircleDrawable
from ..math.vector2d import Vector2D
from ..sprite.sprite import Sprite

import pygame


class CircleSprite(Sprite):
    def __init__(self, id, position=None, radius=1, color="red", *args, **kwargs):
        super().__init__(id, *args, **kwargs)

        if position is None:
            position = Vector2D(0, 0)
        self.radius = radius
        self.position = position

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)
        self.color = pygame.Color(color)

    def tick(self, dt):
        super().tick(dt)

        self.position.x += self.x_velocity * dt
        self.position.y += self.y_velocity * dt

    def set_radius(self, radius):
        self.radius = radius
        self.dirty = True

    def get_drawable(self):
        return CircleDrawable()

    def sync(self, info):
        super().sync(info)
        self.radius = info["data"]["radius"]
        self.position.x = info["x"]
        self.position.y = info["y"]
