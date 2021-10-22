import pygame
from .drawable import Drawable


class PolygonDrawable(Drawable):
    def draw(self, screen, sprite):
        pygame.draw.polygon(screen, sprite.color, sprite.points)
