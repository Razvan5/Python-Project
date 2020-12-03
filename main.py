import sys
import pygame
import spritesheet
import cursor
import tile as tile_class
import random

# example:
mahjong_vertex_dictionary = {
    # center
    1:  (3,  0,  0, 0),
    # bottom left
    2:  (2, -1, -1, 1),
    3:  (2,  1,  1, 2),
    4:  (2,  1, -1, 1),
    5:  (2, -1,  1, 2),
    6:  (1, -2,  2, 5),
    7:  (1,  2, -2, 6),
    8:  (1, -2, -2, 4),
    9:  (1,  2,  2, 5),

    10: (1, -2, 0, 6),
    11: (1, 2, 0, 3),
    12: (1, 0, -2, 3),
    13: (1, 0, 2, 4),

    14: (1, 5, 0.5, 0),
    15: (1, 7, -0.5, 1),
    16: (1, 9, 0.5, 0),
    17: (2, 8, 0, 1),
    18: (2, 10, 0, 0),
    19: (1, 11, -0.5, 1),
    20: (1, 13, 0.5, 1),
 }
game_width, game_height = (1536, 804)
shortener = 0
tile_width, tile_height = (108-shortener, 140-shortener)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((game_width, game_height))


def order_dictionary(mahjong_dictionary):
    mahjong_dictionary = {k: v for k, v in sorted(mahjong_dictionary.items(), key=lambda item: item[1])}
    return mahjong_dictionary


if __name__ == '__main__':

    print("Game is running...")
    background = pygame.image.load("images/backgrounds/normal/Antique.jpg")
    sprite_sheet = spritesheet.SpriteSheet("images/tiles/normal/modern.png")
    pointer = cursor.Cursor("images/others/cursor.png")
    pointer_group = pygame.sprite.Group()
    pointer_group.add(pointer)
    pygame.mouse.set_visible(False)

    mahjong_vertex_dictionary = order_dictionary(mahjong_vertex_dictionary)
    tiles = sprite_sheet.all_sprites(mahjong_vertex_dictionary, tile_width, tile_height, game_width/2, game_height/2)
    tile_group = pygame.sprite.Group()
    print(tiles)
    # for i in range(5):
    #     tile = tile_class.Tile("images/others/tile_hint.png",
    #                            random.randrange(0, game_width),
    #                            random.randrange(0, game_height))
    #     tile_group.add(tile)

    for i in range(len(tiles)):
        print(tiles[i][0])
        tile_group.add(tiles[i][0])

    game_is_running = True
    selected_tile_position = ()
    player_clicks = []

    while game_is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pointer.select_good(pointer, tile_group)
                pos_x, pos_y = pygame.mouse.get_pos()
                print(pos_x, pos_y)

        pygame.display.flip()
        resized_background = pygame.transform.scale(background, (game_width, game_height))
        screen.blit(resized_background, (0, 0))
        tile_group.draw(screen)
        pointer_group.draw(screen)
        pointer_group.update()
        clock.tick(60)

