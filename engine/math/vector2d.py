from __future__ import annotations
import math
from typing import Union


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x=x, y=y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x=x, y=y)

    def scalar_multiply(self, scale):
        self.x *= scale
        self.y *= scale

    def dot(self, other):
        return Vector2D(self.x * other.x + self.y * other.y)

    @property
    def rotation_angle(self):
        return math.atan2(self.y, self.x)

    @property
    def rotation_angle_deg(self):
        return math.degrees(self.rotation_angle())
