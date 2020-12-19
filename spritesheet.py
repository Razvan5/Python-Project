import pygame
import tile
from constants import *
# Used for extracting the surfaces and creating tiles from the sprite sheet


class SpriteSheet(pygame.sprite.Sprite):
    """
        Constructor method, creates a Sprite sheet object used for tile creation\n
        :param filepath: the path for the tiles sprite sheet that must have the tiles places in line and at equal
            distance set by the constant TILE_GAP
    """

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        try:
            self.sprite_sheet = pygame.image.load(filepath).convert()
        except pygame.error as sprite_load_error:
            print(f"Unable to load sprite sheet image:{filepath}")
            raise SystemExit(sprite_load_error)

    def sprite_at(self, identifier,
                  sprite_sheet_x, sprite_sheet_y, tile_width, tile_height, on_screen_x, on_screen_y, layer, tile_type):
        """
        Function responsible for creating a singular Tile object with specific zoom factor, color correction and surface
        and rectangle grouping\n
        :param identifier: unique number for identifying tiles
        :param sprite_sheet_x: the x coordinate in the sprite sheet
        :param sprite_sheet_y: the y coordinate in the sprite sheet
        :param tile_width: the width of the tile
        :param tile_height: the height of the tile
        :param on_screen_x: the absolute x position of the tile on screen
        :param on_screen_y: the absolute y position of the tile on screen
        :param layer: the height attribute of the tile object, used for interactions
        :param tile_type: the type of the tile object, specifies the relative position of the tile in the sprite sheet
            and the the types that can match with it
        :return: tile.Tile()
        """

        self.image = pygame.Surface((tile_width, tile_height))
        # Takes image transparency into account
        # Links a surface with the current sprite
        self.image.blit(self.sprite_sheet, (0, 0), pygame.Rect(sprite_sheet_x, sprite_sheet_y, tile_width, tile_height))
        self.image = pygame.transform.rotozoom(self.image, 0, ZOOM_FACTOR)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(TRANSPARENCY_COLOR)
        self.rect.center = [on_screen_x, on_screen_y]
        # self.image = pygame.transform.scale(self.image, (100, 100))
        new_tile = tile.Tile(identifier, self.image, self.rect, self.rect.center, layer, tile_type)
        return new_tile

    def all_sprites(self, mahjong_tiles_dictionary, middle_x, middle_y):
        """
        Function responsible for creating a list of Tile objects by reading a dictionary with tuples of information\n
        :param mahjong_tiles_dictionary: a dictionary with a unique identifier that has attached the relative
            coordinates, tile layer and tile type in a tuple\n
        :param middle_x: pygame.screen middle x
        :param middle_y: pygame.screen middle y
        :return: list of tile.Tile()
        """

        # returns a vector of
        return [
                [self.sprite_at(
                    identifier,
                    (TILE_WIDTH+TILE_GAP)*sprite_type,    # x position in the sprite sheet image
                    0,                                    # y position
                    TILE_WIDTH,
                    TILE_HEIGHT,
                    (middle_x+TILE_WIDTH/2*x)*ZOOM_FACTOR,     # surface rectangle center x
                    (middle_y+TILE_HEIGHT/2*y)*ZOOM_FACTOR,    # surface rectangle center y
                    layer,                                # the tile layer/height
                    sprite_type),                         # the sprite type (the order in the sprite sheet line)
                    (middle_x+TILE_WIDTH/2*x)*ZOOM_FACTOR, (middle_y+TILE_HEIGHT/2*y)*ZOOM_FACTOR]
                for identifier, (layer, x, y, sprite_type) in mahjong_tiles_dictionary.items()
        ]
