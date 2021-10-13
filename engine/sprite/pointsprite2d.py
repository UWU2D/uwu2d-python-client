from engine.sprite.polygonsprite2d import PolygonSprite2D
from engine.math.vector2d import Vector2D
import math


class PointSprite2D(PolygonSprite2D):
    def __init__(self, id, point=Vector2D(0, 0), *args, **kwargs):
        super().__init__(id, points=[(point.x, point.y)], *args, **kwargs)

    def tick(self, dt):
        super().tick()

    @property
    def point(self):
        return Vector2D(x=self.points[0][0], y=self.points[0][1])

    @property
    def absolute_point(self):
        abs_point = Vector2D(
            x=self.point.x * math.cos(self.absolute_rotation),
            y=self.point.y * math.sin(self.absolute_rotation),
        )
        return abs_point + self.absolute_position_vector

    def get_drawable(self):
        return None

    def sync_info(self):
        info = super().sync_info()

        info.update(
            {
                "type": "PointSprite2D",
            }
        )

        return info
