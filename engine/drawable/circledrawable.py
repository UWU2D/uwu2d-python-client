import pygame
from engine.drawable.drawable import Drawable

class CircleDrawable(Drawable):
    def draw(self, screen, sprite):
        abs_pos_vec = sprite.absolute_position_vector

        center_point = (int(abs_pos_vec.x), int(abs_pos_vec.y))
        if sprite.color is not None:
            pygame.draw.circle(screen, sprite.color, center_point, sprite.radius)
        else:
            pygame.draw.circle(screen, sprite.color, sprite.radius)
