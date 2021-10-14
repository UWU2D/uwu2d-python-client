from engine.drawable.boxdrawable import BoxDrawable
from engine.sprite.sprite import Sprite
from engine.math.vector2d import Vector2D
import math
import pygame


class BoxSprite2D(Sprite):
    def __init__(self, id, scale=Vector2D(x=1, y=1), color="red", *args, **kwargs):

        self.scale_vector = Vector2D(scale.x, scale.y)

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)

        self.color = color

        super().__init__(id, *args, **kwargs)

    def tick(self, dt):
        super().tick()

        if self.collider is not None:
            self.collider.position_vector.x = self.position_vector.x
            self.collider.position_vector.y = self.position_vector.y
            self.collider.scale_vector.x = self.scale_vector.x
            self.collider.scale_vector.y = self.scale_vector.y

    def set_scale_from_points(self, x, y):
        self.scale_vector.x = x
        self.scale_vector.y = y
        self.dirty = True

    def set_scale_from_vector(self, vector):
        self.scale_vector.x = vector.x
        self.scale_vector.y = vector.y
        self.dirty = True

    def set_scale(self, scale):
        self.scale_vector.x = scale.x
        self.scale_vector.y = scale.y

    def get_drawable(self):
        return BoxDrawable()

    def get_points(self):
        center = Vector2D(
            x=self.position_vector.x + self.scale_vector.x / 2.0,
            y=self.position_vector.y + self.scale_vector.y / 2.0,
        )

        width = self.scale_vector.x
        height = self.scale_vector.y
        angle = self.rotation

        cos_ang = math.cos(angle)
        sin_ang = math.sin(angle)

        half_width = width / 2
        half_height = height / 2

        top_right = Vector2D(
            x=center.x + (half_width * cos_ang) - (half_height * sin_ang),
            y=center.y + (half_width * sin_ang) + (half_height * cos_ang),
        )
        top_left = Vector2D(
            x=center.x - (half_width * cos_ang) - (half_height * sin_ang),
            y=center.y - (half_width * sin_ang) + (half_height * cos_ang),
        )
        bottom_left = Vector2D(
            x=center.x - (half_width * cos_ang) + (half_height * sin_ang),
            y=center.y - (half_width * sin_ang) - (half_height * cos_ang),
        )
        bottom_right = Vector2D(
            x=center.x + (half_width * cos_ang) + (half_height * sin_ang),
            y=center.y + (half_width * sin_ang) - (half_height * cos_ang),
        )

        return [
            (top_left.x, top_left.y),
            (top_right.x, top_right.y),
            (bottom_right.x, bottom_right.y),
            (bottom_left.x, bottom_left.y),
        ]

    def sync_info(self) -> dict:
        info = super().sync_info()

        info.update(
            {
                "w": self.scale_vector.x,
                "h": self.scale_vector.y,
                "type": "BoxSprite2D",
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

        self.scale_vector.x = info.get("w", self.scale_vector.x)
        self.scale_vector.y = info.get("h", self.scale_vector.y)

        if self.color is None:
            self.color = pygame.Color(0, 0, 0, 1)

        if "color" in info:
            color_info = info["color"]
            self.color.r = color_info.get("r", self.color.r)
            self.color.g = color_info.get("g", self.color.g)
            self.color.b = color_info.get("b", self.color.b)
            self.color.a = color_info.get("a", self.color.a)
