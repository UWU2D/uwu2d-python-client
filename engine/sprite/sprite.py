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
        position=Vector2D(x=0, y=0),
        rotation=0,
        velocity=Vector2D(x=0, y=0),
        rotational_velocity=0,
        enable_collider=False,
        debug_name=None,
    ):

        self.id = id
        self.dirty = True
        self.position_vector = Vector2D(position.x, position.y)
        self.rotation = rotation
        self.velocity_vector = Vector2D(velocity.x, velocity.y)
        self.rotational_velocity = rotational_velocity

        self.collider = None
        self.debug_name = debug_name

        self.two_pi = math.pi * 2
        self.drawable = self.get_drawable()

        self.parent = None
        self.children = []

    def tick(self, dt):
        self.position_vector += self.velocity_vector
        self.rotation += self.rotational_velocity

        # normalize the rotation
        if self.rotation > self.two_pi:
            self.rotation -= self.two_pi
        elif self.rotation < 0:
            self.rotation += self.two_pi

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parent = self

    def get_drawable(self):
        return None

    @property
    def absolute_position_vector(self):
        if self.parent is None:
            return self.position_vector
        else:
            abs_rot = self.absolute_rotation
            abs_pos = self.position_vector + self.parent.absolute_position_vector
            return engine_math.rotate_point(
                self.parent.absolute_position_vector, abs_pos, abs_rot
            )
            return Vector2D(
                abs_pos.x * math.cos(abs_rot), abs_pos.y * math.sin(abs_rot)
            )

    @property
    def absolute_rotation(self):
        if self.parent is None:
            return self.rotation
        else:
            return self.rotation + self.parent.absolute_rotation

    @property
    def absolute_velocity_vector(self):
        if self.parent is None:
            return self.velocity_vector
        else:
            return self.velocity_vector + self.parent.absolute_velocity_vector

    @property
    def absolute_rotational_velocity(self):
        if self.parent is None:
            return self.rotational_velocity
        else:
            return self.rotational_velocity + self.parent.absolute_rotational_velocity

    def sync_info(self):
        return {
            "x": self.position_vector.x,
            "y": self.position_vector.y,
            "vx": self.velocity_vector.x,
            "vy": self.velocity_vector.y,
            "rot": self.rotation,
            "vrot": self.rotational_velocity,
            "id": self.id,
            "parent": self.parent.id if self.parent is not None else None,
            "children": [c.id for c in self.children],
        }

    def from_sync_info(self, info):

        color = info["data"].get("color", "pink")
        self.color = pygame.Color(color)

        self.position_vector.x = info.get("x", self.position_vector.x)
        self.position_vector.y = info.get("y", self.position_vector.y)
        self.velocity_vector.x = info.get("vx", self.velocity_vector.x)
        self.velocity_vector.y = info.get("vy", self.velocity_vector.y)
        self.rotation = info.get("rot", self.rotation)
        self.rotational_velocity = info.get("vrot", self.rotational_velocity)
