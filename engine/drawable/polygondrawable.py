import pygame
from engine.drawable.drawable import Drawable


class PolygonDrawable(Drawable):
    def draw(self, screen, sprite):
        points = sprite.absolute_points

        if sprite.color is not None:
            pygame.draw.polygon(screen, sprite.color, points)
        else:
            pygame.draw.polygon(screen, pygame.color.Color(0, 0, 0, 0), points)
