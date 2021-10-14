import pygame
from engine.drawable.drawable import Drawable


class PolygonDrawable(Drawable):
    def draw(self, screen, sprite):

        if sprite.color is not None:
            pygame.draw.polygon(screen, sprite.color, sprite.points)
        else:
            pygame.draw.polygon(screen, pygame.color.Color(0, 0, 0, 0), sprite.points)
