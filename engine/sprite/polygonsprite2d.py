from engine.drawable.polygondrawable import PolygonDrawable
from engine.sprite.sprite import Sprite
from engine.math.vector2d import Vector2D
import engine.math.math as engine_math

import pygame


class PolygonSprite2D(Sprite):
    def __init__(self, id, points=None, color="red", *args, **kwargs):

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)

        if points is None:
            points = []

        self.color = color

        self.points = list(points)

        super().__init__(id, *args, **kwargs)

    def tick(self, dt):
        super().tick(dt)

    def get_drawable(self):
        return PolygonDrawable()

    def from_sync_info(self, info):
        super().from_sync_info(info)

        points = info["data"].get("points", [])
        self.points[:] = [(p["x"], p["y"]) for p in points]
