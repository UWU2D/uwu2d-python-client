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

        self.x_velocity = 0
        self.y_velocity = 0

        # TODO Accel?
        self.x_accel = 0
        self.y_accel = 0

    def tick(self, dt):
        pass

    def get_drawable(self):
        return None

    def from_sync_info(self, info):
        data = info["data"]

        if 'rgba' in data:
            rgba = data['rgba']
            self.color = pygame.color(rgba[0], rgba[1], rgba[2], rgba[3] * 255)
        elif 'color' in data:
            self.color = data['color']

        self.x_velocity = data.get("xVelocity", self.x_velocity)
        self.y_velocity = data.get("yVelocity", self.y_velocity)
        self.x_accel = data.get("xAccel", self.x_accel)
        self.y_accel = data.get("yAccel", self.y_accel)
