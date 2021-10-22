from .vector2d import Vector2D
import math


def clamp(val, low, high):
    if val < low:
        return low
    elif val > high:
        return high
    else:
        return val


def rotate_point(center, point, rotation):
    if rotation == 0:
        return point

    cos_ang = math.cos(rotation)
    sin_ang = math.sin(rotation)

    rx = center.x + (cos_ang * (point.x - center.x)) - (sin_ang * (point.y - center.y))
    ry = center.y + (sin_ang * (point.x - center.x)) + (cos_ang * (point.y - center.y))

    return Vector2D(x=rx, y=ry)
