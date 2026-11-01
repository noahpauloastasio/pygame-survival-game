import pygame
from settings import *
from settings import TILESIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(*groups)

        if image:
            # visible tile or prop
            self.image = image
            self.rect = self.image.get_rect(topleft=pos)

        else:
            # invisible collision object
            # give it a placeholder image
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

        # hitbox used by collision system
        self.hitbox = self.rect.copy()
