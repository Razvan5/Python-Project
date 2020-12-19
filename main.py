import sys
import pygame
import spritesheet
import cursor
import random
import initialize
import tile
from constants import *

# example:
mahjong_tiles_dictionary = {
    # center
    1:  (3,  0,  0, 0),
    2:  (2, -1, -1, 1),
    3:  (2,  1,  1, 2),
    4:  (2,  1, -1, 1),
    5:  (2, -1,  1, 2),
    6:  (1, -2,  2, 5),
    7:  (1,  2, -2, 6),
    8:  (1, -2, -2, 4),
    9:  (1,  2,  2, 5),

    10: (1, -2,  0, 6),
    11: (1,  2,  0, 3),
    12: (1,  0, -2, 3),
    13: (1,  0,  2, 4),

    14: (1, 5,  0.5,  0),
    15: (1, 7, -0.5,  1),
    16: (1, 9,  0.5,  0),
    17: (2, 8,  0,    1),
    18: (2, 10, 0,    0),
    19: (1, 11, -0.5, 1),
    20: (1, 13, 0.5,  1),

    21: (1, -10, -3.5,  1),
    22: (1, -10, -1.5,  1),
    23: (1, -10, 0.5,  1),
    24: (1, -10, 2.5,  1),
    25: (1, -10, 4.5,  1),
    26: (1, -10, 6.5,  1),
    # 27: (1, -10, 8.5,  1),

 }

# initialize the game
pygame.init()
# clock used for time display
clock = pygame.time.Clock()
# initializing the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def shuffle():
    """
    Shuffles the tile types from the tiles dictionary, a global variable
    """

    remaining_tile_types = [tile_type for (a, b, c, tile_type) in mahjong_tiles_dictionary.values()]
    random.shuffle(remaining_tile_types)
    for identifier, (layer, x, y, sprite_type) in mahjong_tiles_dictionary.items():
        mahjong_tiles_dictionary.update({identifier: (layer, x, y, remaining_tile_types.pop())})


def init_level():
    """
    initializes a level using the initialize.Initialize() module, overwrites the global mahjong dictionary
    """

    test_level = {}
    initialize_level = initialize.Initialize(test_level)
    # first(bottom) layer
    initialize_level.draw_line(-4, 20, static_coord=-3.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(0, 16, static_coord=-1.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(-2, 18, static_coord=0.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(-4, 20, static_coord=2.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(-4, 20, static_coord=4.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(-2, 18, static_coord=6.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(0, 16, static_coord=8.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_line(-4, 20, static_coord=10.5, layer_height=1, orientation='horizontal')
    initialize_level.draw_piece(-6, 3.5, 1)
    initialize_level.draw_piece(20, 3.5, 1)

    # middle-first layer
    initialize_level.draw_line(1, 15, static_coord=-1, layer_height=2, orientation='horizontal')
    initialize_level.draw_line(1, 15, static_coord=1, layer_height=2, orientation='horizontal')
    initialize_level.draw_line(1, 15, static_coord=3, layer_height=2, orientation='horizontal')
    initialize_level.draw_line(1, 15, static_coord=5, layer_height=2, orientation='horizontal')
    initialize_level.draw_line(1, 15, static_coord=7, layer_height=2, orientation='horizontal')

    # middle-second layer
    initialize_level.draw_line(2, 12, static_coord=-0.5, layer_height=3, orientation='horizontal')
    initialize_level.draw_line(2, 12, static_coord=1.5, layer_height=3, orientation='horizontal')
    initialize_level.draw_line(2, 12, static_coord=3.5, layer_height=3, orientation='horizontal')
    initialize_level.draw_line(2, 12, static_coord=5.5, layer_height=3, orientation='horizontal')

    # middle-third layer
    initialize_level.draw_line(5, 9, static_coord=0, layer_height=4, orientation='horizontal')
    initialize_level.draw_line(5, 9, static_coord=2, layer_height=4, orientation='horizontal')
    initialize_level.draw_line(5, 9, static_coord=4, layer_height=4, orientation='horizontal')

    # top-layer
    initialize_level.draw_piece(6, 2, 5)

    global mahjong_tiles_dictionary
    mahjong_tiles_dictionary = test_level


def order_dictionary():
    """
    The function orders the tiles in the tile dictionary so the sprites are rendered in a correct 3D fashion with little
    to no overlaps\n
    """

    # the tiles are ordered so the pygame rendering is not overlapping the wrong tiles.
    global mahjong_tiles_dictionary
    mahjong_tiles_dictionary = {k: v for k, v in sorted(mahjong_tiles_dictionary.items(), key=lambda item: item[1])}


def initialize_tiles():
    """
    The function uses the global mahjong dictionary to construct pygame.sprite.Group() with the properties found in the
    dictionary\n
    :return: a sprite group containing all the tiles to be rendered and interacted with
    :rtype: pygame.sprite.Group()
    """
    sprite_sheet = spritesheet.SpriteSheet(TILES_TEXTURES)
    # Extracting sprites out of the linear sprite sheet
    tiles = sprite_sheet.all_sprites(
        mahjong_tiles_dictionary,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2)
    tile_sprite_group = pygame.sprite.Group()

    # Constructing the tile group for rendering and collision detection
    for i in range(len(tiles)):
        # print(tiles[i][0])
        tile_sprite_group.add(tiles[i][0])

    return tile_sprite_group


def initialize_game():
    """
    Initializes a tuple of variables used by the main while loop to perform certain actions\n
    :return: a tuple made of a background surface, a cursor.Cursor() object, a cursor sprite.Group(), a tile
    sprite.Group() and a boolean variable to decide the game state
    """
    # Loading all the game sprites + objects for the tile and cursor objects
    # Cursor, Tile and SpriteSheet are inheriting the pygame.sprite.Sprite class
    background_surface = pygame.image.load(BACKGROUND_TEXTURE)
    init_level()
    order_dictionary()
    pointer_object = cursor.Cursor(CURSOR_TEXTURE, mahjong_tiles_dictionary, screen)
    # Changing the cursor texture and adding it to a custom group
    pointer_sprite_group = pygame.sprite.Group()
    pointer_sprite_group.add(pointer_object)
    pygame.mouse.set_visible(False)

    # Extracting sprites out of the linear sprite sheet
    tile_sprite_group = initialize_tiles()

    is_game_running = True

    game_music = pygame.mixer.Sound(GAME_MUSIC[random.randint(0, 1)])
    game_music.play(30)

    return background_surface, pointer_object, pointer_sprite_group, tile_sprite_group, is_game_running


def check_unwinnable_game(tile_sprite_group):
    """
    Checks every tile for potential pairings and if no pairings are possible for all tiles on the screen\n
    :param tile_sprite_group: the tile group
    :type: pygame.sprite.Group()
    :return: returns if the game is unwinnable
    """

    if len(tile_sprite_group) == 0:
        return False
    for compared_tile in tile_sprite_group:
        if not cursor.is_tile_covered(compared_tile, tile_sprite_group) \
                and not cursor.is_tile_surrounded(compared_tile, tile_sprite_group):
            for comparing_tile in tile_sprite_group:
                if isinstance(comparing_tile, tile.Tile) and isinstance(compared_tile, tile.Tile) \
                    and comparing_tile != compared_tile and comparing_tile.tile_type == compared_tile.tile_type \
                    and not cursor.is_tile_covered(comparing_tile, tile_sprite_group) \
                        and not cursor.is_tile_surrounded(comparing_tile, tile_sprite_group):
                    return False
    return True


def render_text(text_group, text_location, text_shadow_location):
    """
    Renders different text groups on screen for less game loop cluttering\n
    :param text_group: a tuple made out of the text surface and text shadow surface
    :param text_location: the texts locations
    :type text_location: tuple of ints
    :param text_shadow_location: the location of the text's shadow
    :type text_shadow_location: tuple of ints
    """
    if len(text_group):
        screen.blit(text_group[0], text_location)
        screen.blit(text_group[1], text_shadow_location)


if __name__ == '__main__':

    print("Game is running...")

    background, pointer, pointer_group, tile_group, game_is_running = initialize_game()
    resized_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    shuffle_message = []
    win_message = []

    while game_is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                continue_game = pointer.select_tile(tile_group)
                if check_unwinnable_game(tile_group):
                    font = pygame.font.Font(GAME_FONT, GAME_FONT_SIZE)
                    text = font.render(SHUFFLE_TEXT, True, pygame.color.Color("red"))
                    text_shadow = font.render(SHUFFLE_TEXT, True, GAME_FONT_SHADOW_COLOR)
                    shuffle_message.append(text_shadow)
                    shuffle_message.append(text)
                if continue_game is False:
                    font = pygame.font.Font(GAME_FONT, GAME_FONT_SIZE)
                    text = font.render(FINISH_TEXT_1, True, GAME_FONT_COLOR)
                    text_shadow = font.render(FINISH_TEXT_1, True, GAME_FONT_SHADOW_COLOR)
                    win_message.append(text_shadow)
                    win_message.append(text)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    mahjong_tiles_dictionary = pointer.get_mahjong_dictionary()
                    shuffle()
                    tile_group = initialize_tiles()
                    shuffle_message.clear()
                    pointer.previous_tile = None
                if win_message:
                    pygame.quit()
                    sys.exit()
        # rendering all the sprites, background and texts
        pygame.display.flip()
        screen.blit(resized_background, (0, 0))
        tile_group.draw(screen)
        render_text(win_message,
                    (SCREEN_WIDTH // 15, SCREEN_HEIGHT // 2),
                    (SCREEN_WIDTH // 15 - 4, SCREEN_HEIGHT // 2))
        render_text(shuffle_message,
                    (SCREEN_WIDTH // 15, SCREEN_HEIGHT // 2),
                    (SCREEN_WIDTH // 15 - 4, SCREEN_HEIGHT // 2))
        pointer_group.draw(screen)
        pointer_group.update()
        clock.tick(60)
