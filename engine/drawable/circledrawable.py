import pygame
from engine.drawable.drawable import Drawable


class CircleDrawable(Drawable):
    def draw(self, screen, sprite):

        center_point = (int(sprite.position.x), int(sprite.position.y))
        if sprite.color is not None:
            pygame.draw.circle(screen, sprite.color, center_point, sprite.radius)
        else:
            pygame.draw.circle(screen, sprite.color, sprite.radius)
