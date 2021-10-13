from engine.drawable.polygondrawable import PolygonDrawable
from engine.sprite.sprite import Sprite
from engine.math.vector2d import Vector2D
import engine.math.math as engine_math

import pygame


class PolygonSprite2D(Sprite):
    def __init__(self, id, points=None, color=None, *args, **kwargs):

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)

        if points is None:
            points = []

        self.color = color

        self.points = list(points)

        super().__init__(id, *args, **kwargs)

    def tick(self, dt):
        super().tick()

        if self.collider is not None:
            self.collider.position_vector.x = self.position_vector.x
            self.collider.position_vector.y = self.position_vector.y
            self.collider.scale_vector.x = self.scale_vector.x
            self.collider.scale_vector.y = self.scale_vector.y

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

        if "points" in info:
            self.points[:] = [(p["x"], p["y"]) for p in info["points"]]

        if self.color is None:
            self.color = pygame.Color(0, 0, 0, 1)

        if "color" in info:
            color_info = info["color"]
            self.color.r = color_info.get("r", self.color.r)
            self.color.g = color_info.get("g", self.color.g)
            self.color.b = color_info.get("b", self.color.b)
            self.color.a = color_info.get("a", self.color.a)
