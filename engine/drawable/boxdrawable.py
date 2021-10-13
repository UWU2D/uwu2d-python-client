import pygame
from engine.drawable.drawable import Drawable


class BoxDrawable(Drawable):
    def draw(self, screen, sprite):

        if sprite.rotation == 0 and sprite.rotational_velocity == 0:
            self.draw_no_rotation(screen, sprite)
        else:
            self.draw_with_rotation(screen, sprite)

    def draw_no_rotation(self, screen, sprite):
        abs_pos_vec = sprite.absolute_position_vector

        rect = pygame.Rect(
            abs_pos_vec.x, abs_pos_vec.y, sprite.scale_vector.x, sprite.scale_vector.y
        )

        if sprite.color is not None:
            pygame.draw.rect(screen, sprite.color, rect)
        else:
            pygame.draw.rect(screen, rect)

    def draw_with_rotation(self, screen, sprite):
        points = sprite.get_points()

        if sprite.color is not None:
            pygame.draw.polygon(screen, sprite.color, points)
        else:
            pygame.draw.polygon(screen, points)
