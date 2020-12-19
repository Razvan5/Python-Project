import pygame
# This class is used to hold data about individual tiles


class Tile(pygame.sprite.Sprite):
    """
    Constructor method, creates a Tile object\n
    :param identifier: tile identifier
    :type identifier: positive int
    :param image: pygame.Surface the sprite of the tile
    :type image: pygame.Surface()
    :param rect: pygame.Rect the clickable area of the tile
    :type rect: pygame.Rect()
    :param center: tuple of coordinates for the rect center
    :type center: tuple
    :param layer: the height of the tile, affects interactions
    :type layer: positive int
    :param tile_type: the type of the tile, affects interactions
    :type tile_type: positive int
    """
    def __init__(self, identifier, image, rect, center, layer, tile_type):

        super().__init__()
        self.identifier = identifier
        self.image = image
        self.locked_image = self.image.copy()
        self.rect = rect
        self.rect.center = center
        self.layer = layer
        self.tile_type = tile_type
