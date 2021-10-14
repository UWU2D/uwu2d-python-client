from engine.drawable.circledrawable import CircleDrawable
from engine.sprite.sprite import Sprite

import pygame


class CircleSprite(Sprite):
    def __init__(self, id, radius=1, color="red", *args, **kwargs):

        self.radius = radius

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)

        self.color = pygame.Color(color)

        super().__init__(id, *args, **kwargs)

    def tick(self, dt):
        super().tick(dt)

        if self.collider is not None:
            self.collider.position_vector.x = self.position_vector.x
            self.collider.position_vector.y = self.position_vector.y
            self.collider.radius = self.radius

    def set_radius(self, radius):
        self.radius = radius
        self.dirty = True

    def get_drawable(self):
        return CircleDrawable()

    def sync_info(self):
        info = super().sync_info()

        info.update(
            {
                "r": self.radius,
                "type": "CircleSprite",
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

        self.radius = info["data"]["radius"]

        if self.color is None:
            self.color = pygame.Color(0, 0, 0, 1)

        if "color" in info:
            color_info = info["color"]
            self.color.r = 255  # color_info.get("r", self.color.r)
            self.color.g = color_info.get("g", self.color.g)
            self.color.b = color_info.get("b", self.color.b)
            self.color.a = color_info.get("a", self.color.a)
