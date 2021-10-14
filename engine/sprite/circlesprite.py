from engine.drawable.circledrawable import CircleDrawable
from engine.math.vector2d import Vector2D
from engine.sprite.sprite import Sprite

import pygame


class CircleSprite(Sprite):
    def __init__(
        self, id, position=Vector2D(0, 0), radius=1, color="red", *args, **kwargs
    ):

        self.radius = radius
        self.position = position
        if color is not None and isinstance(color, str):
            color = pygame.Color(color)

        self.color = pygame.Color(color)

        super().__init__(id, *args, **kwargs)

    def tick(self, dt):
        super().tick(dt)

    def set_radius(self, radius):
        self.radius = radius
        self.dirty = True

    def get_drawable(self):
        return CircleDrawable()

    def from_sync_info(self, info):
        super().from_sync_info(info)
        self.radius = info["data"]["radius"]
        self.color = info["data"].get("color", self.color)
        self.position.x = info["x"]
        self.position.y = info["y"]
