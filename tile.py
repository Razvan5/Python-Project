import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, image, rect, center, layer, tile_type):
        super().__init__()
        self.image = image
        self.locked_image = self.image.copy()
        self.rect = rect
        self.rect.center = center
        self.layer = layer
        self.tile_type = tile_type
