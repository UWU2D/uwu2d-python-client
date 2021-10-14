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

    @property
    def relative_points(self):
        center = self.position_vector
        angle = self.rotation

        rotated_points = []

        for point in self.points:
            rot = engine_math.rotate_point(
                center=center,
                point=Vector2D(x=point[0] + center.x, y=point[1] + center.y),
                rotation=angle,
            )
            rotated_points.append((rot.x, rot.y))

        return rotated_points

    @property
    def absolute_points(self):
        abs_pos_vec = self.absolute_position_vector
        abs_angle = self.absolute_rotation

        rotated_points = []

        for point in self.points:
            rot = engine_math.rotate_point(
                center=abs_pos_vec,
                point=Vector2D(x=point[0] + abs_pos_vec.x, y=point[1] + abs_pos_vec.y),
                rotation=abs_angle,
            )
            rotated_points.append((rot.x, rot.y))

        return rotated_points

    def sync_info(self):
        info = super().sync_info()

        points = []
        info.update(
            {
                "points": [{"x": p[0], "y": p[1]} for p in self.points],
                "type": "PolygonSprite2D",
                "color": {
                    "r": self.color.r,
                    "g": self.color.g,
                    "b": self.color.b,
                    "a": self.color.a,
                },
            }
        )

        return info

    def from_sync_info(self, info):
        super().from_sync_info(info)

        points = info["data"].get("points", [])

        self.points[:] = [(p["x"], p["y"]) for p in points]
