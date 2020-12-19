import pygame
import tile
from constants import *


def select_highest_tile(collided_list):
    """
    Selects the tile with the highest layer number\n
    :param collided_list: the list of tiles the cursor collided with when it clicked
    :type collided_list: list(tile.Tile())
    :return: a tile
    :rtype: tile.Tile()
    """

    highest_layer = 0
    selected_tile = pygame.sprite.Sprite()
    for sprite in collided_list:
        if isinstance(sprite, tile.Tile):
            if highest_layer < sprite.layer:
                highest_layer = sprite.layer
                selected_tile = sprite
    return selected_tile


def is_tile_covered(selected_tile, tile_group):
    """
    Boolean decider if the tile is covered or not using the pygame.sprite.spritecollide()\n
    :param selected_tile: the tile selected by the player
    :param tile_group: all the tiles on the screen
    :return: if the tile is covered by another tile higher in level or not
    :rtype: bool
    """

    is_covered = False
    for intersected_sprite in pygame.sprite.spritecollide(selected_tile, tile_group, False):
        if isinstance(intersected_sprite, tile.Tile) and intersected_sprite.layer > selected_tile.layer:
            is_covered = True
            break
    return is_covered


def is_tile_surrounded(selected_tile, tile_group):
    """
    Boolean function returning if a tile is blocked by at least one tile from both directions, using two tile.Tile()
    objects that detect collisions\n
    :param selected_tile: the tile selected by the player
    :type selected_tile: tile.Tile()
    :param tile_group: all the tiles on the screen
    :type tile_group: pygame.sprite.Group()
    :return: if the tile is locked on the left and right side and they are on the same layer
    :return type: bool
    """

    is_locked_between_right = False
    is_locked_between_left = False

    selected_width = selected_tile.rect.width
    center_x, center_y = selected_tile.rect.center
    center = (center_x - selected_width / 3, center_y)
    selected_rect = pygame.Rect((selected_tile.rect.x - selected_tile.rect.width / 2,
                                 selected_tile.rect.y,
                                 selected_tile.rect.width, selected_tile.rect.height))
    checking_tile_right = tile.Tile(0, selected_tile.image,
                                    selected_rect, center, selected_tile.layer, selected_tile.tile_type)

    selected_width = selected_tile.rect.width
    center_x, center_y = selected_tile.rect.center
    center = (center_x + selected_width / 3, center_y)
    selected_rect = pygame.Rect((selected_tile.rect.x + selected_tile.rect.width / 2,
                                 selected_tile.rect.y,
                                 selected_tile.rect.width, selected_tile.rect.height))
    checking_tile_left = tile.Tile(0, selected_tile.image,
                                   selected_rect, center, selected_tile.layer, selected_tile.tile_type)

    if len(pygame.sprite.spritecollide(checking_tile_right, tile_group, False)) >= 2 \
            and len(pygame.sprite.spritecollide(checking_tile_left, tile_group, False)) >= 2:
        for right_tile in pygame.sprite.spritecollide(checking_tile_right, tile_group, False):
            if isinstance(right_tile, tile.Tile) and \
                    right_tile.layer == selected_tile.layer and \
                    right_tile.rect.center != selected_tile.rect.center and \
                    right_tile.rect.center != checking_tile_right.rect.center:
                is_locked_between_right = True
        for left_tile in pygame.sprite.spritecollide(checking_tile_left, tile_group, False):
            if isinstance(left_tile, tile.Tile) and \
                    left_tile.layer == selected_tile.layer and \
                    left_tile.rect.center != selected_tile.rect.center and \
                    left_tile.rect.center != checking_tile_left.rect.center:
                is_locked_between_left = True
    return is_locked_between_right is True and is_locked_between_left is True


class Cursor(pygame.sprite.Sprite):
    """
    Class used for game logic, initializes a cursor object with a custom texture, memorizes the dictionary for easy
    tile manipulation\n
    :param sprite_path: the relative path of the cursor image
    :type sprite_path: constant str
    :param mahjong_dictionary: the tile dictionary used for identifying, erasing, shuffling and matching tiles
    :type mahjong_dictionary: dict
    :param screen: the visible area where the game is performed
    :type screen: pygame.display()
    """

    def __init__(self, sprite_path, mahjong_dictionary, screen):
        super().__init__()
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.tile_match_sound = pygame.mixer.Sound("sounds/good_select.ogg")
        self.empty_select_sound = pygame.mixer.Sound("sounds/tile_select.ogg")
        self.previous_tile = None
        self.current_tile = None
        self.mahjong_dictionary = mahjong_dictionary
        self.screen = screen

    def select_tile(self, tile_group):
        """
        Method used for selecting 2 tiles, checking if they are compatible and returning the state of the game and plays
        different sounds for clicking and matching tiles\n
        :param tile_group: the tiles rendered on screen
        :type tile_group: pygame.sprite.Group()
        :return: if the game can end
        :rtype: bool
        """

        self.empty_select_sound.play()
        collided_list = pygame.sprite.spritecollide(self, tile_group, False)
        # Checks if there are any collided tiles
        if len(collided_list) > 0:
            # layer 1 is the lowest and it continues up to the max layer in the dict from main
            selected_tile = select_highest_tile(collided_list)
            # Checks if the tile is covered by at least another tile
            if is_tile_covered(selected_tile, tile_group) is False:
                # checks if the tile is only blocked from the right or from the left
                # the tile is already checked for tiles above it
                if is_tile_surrounded(selected_tile, tile_group) is False:
                    # a sprite initialized by the Cursor object which tracks the previous tile
                    self.check_tile_match(selected_tile, tile_group)
        return self.check_game_state()

    def check_tile_match(self, selected_tile, tile_group):
        """
        Checks if two tiles can be matched, highlights the first clicked tile and alters the screen and dictionary if it
        succeeds\n
        :param selected_tile: the currently selected tile
        :type selected_tile: tile.Tile()
        :param tile_group: all the rendered tiles
        """
        if self.previous_tile is None:
            # we get the first sprite and draw the selection ring on it
            self.previous_tile = selected_tile
            selection_color = SELECTION_COLOR  # red-orange
            # selection rectangle around selected tile
            pygame.draw.rect(
                selected_tile.image,
                selection_color,
                pygame.Rect(0, 0, SELECTION_WIDTH, SELECTION_HEIGHT),
                width=SELECTION_BORDER_WIDTH,
                border_radius=SELECTION_BORDER_RADIUS
            )
        else:
            # there is another tile in the list,
            # lets check if they have the same type and are not the same tile
            if isinstance(self.previous_tile, tile.Tile) \
                    and self.previous_tile.tile_type == selected_tile.tile_type \
                    and self.previous_tile.rect.center != selected_tile.rect.center:

                # deleting the tiles and resetting selected tiles for the next tile match
                self.mahjong_dictionary.pop(selected_tile.identifier)
                self.mahjong_dictionary.pop(self.previous_tile.identifier)
                selected_tile.kill()
                self.previous_tile.kill()
                self.previous_tile = None
                self.tile_match_sound.play()
                # print(self.mahjong_dictionary)
            else:
                # there was no match but we still reset the vector
                self.previous_tile = None
                for any_tile in tile_group:
                    any_tile.image = any_tile.locked_image.copy()

    def check_game_state(self):
        """
        :return: Returns the state mahjong_dictionary is empty
        :rtype: bool
        """

        if len(self.mahjong_dictionary) == 0:
            return False
        return True

    def update(self):
        """
        Overrides a method in the pygame.sprite.Sprite() class and changes the cursor sprite to be at the same position
        as the mouse cursor\n
        """

        self.rect.center = pygame.mouse.get_pos()

    def get_mahjong_dictionary(self):
        """
        Getter used by the shuffle function in the main module\n
        :return: a modified dictionary
        :rtype: dict
        """
        return self.mahjong_dictionary
