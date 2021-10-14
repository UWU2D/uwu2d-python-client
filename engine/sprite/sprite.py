from __future__ import annotations

import pygame
from engine.drawable.drawable import Drawable
import math
from engine.math.vector2d import Vector2D
import engine.math.math as engine_math


class Sprite:
    def __init__(
        self,
        id,
        debug_name=None,
    ):
        self.color = pygame.Color("pink")

        self.id = id
        self.debug_name = debug_name
        self.drawable = self.get_drawable()

    def tick(self, dt):
        pass

    def get_drawable(self):
        return None

    def from_sync_info(self, info):
        self.color = info["data"].get("color", self.color)
