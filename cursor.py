import pygame
import tile


class Cursor(pygame.sprite.Sprite):
    def __init__(self, sprite_path):
        super().__init__()
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.tile_select = pygame.mixer.Sound("sounds/good_select.ogg")
        self.empty_select = pygame.mixer.Sound("sounds/tile_select.ogg")
        self.selected_tiles = []

    def select_good(self, cursor, tile_group):
        self.empty_select.play()
        collided_list = pygame.sprite.spritecollide(cursor, tile_group, False)
        highest_layer = 0
        selected_sprite = pygame.sprite.Sprite()
        for sprite in collided_list:
            if highest_layer < sprite.layer:
                highest_layer = sprite.layer
                selected_sprite = sprite
            # print(f' Layer :{sprite1.layer}')
            # print(f' Type: {sprite1.tile_type+1}')
        if len(collided_list) > 0:
            # print(pygame.sprite.spritecollide(selected_sprite, tile_group, False))
            is_covered = False
            for intersected_sprite in pygame.sprite.spritecollide(selected_sprite, tile_group, False):
                if intersected_sprite.layer > selected_sprite.layer:
                    is_covered = True
                    break
                # print(f'{i.rect} {i.layer}')
            if is_covered is False:

                is_locked_between1 = False
                is_locked_between2 = False
                selected_width = selected_sprite.rect.width
                center_x, center_y = selected_sprite.rect.center
                print(selected_sprite.rect)
                center = (center_x - selected_width/2, center_y)
                selected_rect = pygame.Rect((selected_sprite.rect.x - selected_sprite.rect.width/2, selected_sprite.rect.y, selected_sprite.rect.width, selected_sprite.rect.height))
                checking_tile1 = tile.Tile(selected_sprite.image, selected_rect, center, selected_sprite.layer, selected_sprite.tile_type)
                selected_width = selected_sprite.rect.width
                center_x, center_y = selected_sprite.rect.center
                center = (center_x + selected_width/2, center_y)
                selected_rect = pygame.Rect((selected_sprite.rect.x + selected_sprite.rect.width/2, selected_sprite.rect.y, selected_sprite.rect.width, selected_sprite.rect.height))
                checking_tile2 = tile.Tile(selected_sprite.image, selected_rect, center, selected_sprite.layer, selected_sprite.tile_type)
                if len(pygame.sprite.spritecollide(checking_tile1, tile_group, False)) >= 2 and len(pygame.sprite.spritecollide(checking_tile2, tile_group, False)) >= 2:
                    for t1 in pygame.sprite.spritecollide(checking_tile1, tile_group, False):
                        if t1.layer == selected_sprite.layer and t1.rect.center != selected_sprite.rect.center and t1.rect.center != checking_tile1.rect.center:
                            print(f'{t1.layer} {selected_sprite.layer} {t1.rect.center} {selected_sprite.rect.center} {t1.rect.center} {checking_tile1.rect.center}')
                            is_locked_between1 = True
                    for t2 in pygame.sprite.spritecollide(checking_tile2, tile_group, False):
                        if t2.layer == selected_sprite.layer and t2.rect.center != selected_sprite.rect.center and t2.rect.center != checking_tile2.rect.center:
                            print(f'{t2.layer} {selected_sprite.layer} {t2.rect.center} {selected_sprite.rect.center} {t2.rect.center} {checking_tile1.rect.center} {t2.tile_type}')
                            is_locked_between2 = True

                print(pygame.sprite.spritecollide(checking_tile1, tile_group, False))
                for i in pygame.sprite.spritecollide(checking_tile1, tile_group, False):
                    print(f'{i.rect.center} {i.layer}')
                print(pygame.sprite.spritecollide(checking_tile2, tile_group, False))
                for i in pygame.sprite.spritecollide(checking_tile2, tile_group, False):
                    print(f'{i.rect.center} {i.layer}')

                if is_locked_between1 is False or is_locked_between2 is False:
                    if len(self.selected_tiles) == 0:
                        self.selected_tiles.append(selected_sprite)
                        self.selected_tiles.append(selected_sprite.tile_type)
                        print(f' Click1 {self.selected_tiles[1]} {selected_sprite.tile_type} {selected_sprite.rect.center}')
                        pygame.draw.rect(
                            selected_sprite.image,
                            (30, 10, 210, 1),
                            pygame.Rect(0, 0, selected_sprite.rect.width, selected_sprite.rect.height),
                            width=30)
                        # this detects colliding rectangles
                    else:
                        print(f' Click2 {self.selected_tiles[1]} {selected_sprite.tile_type} {selected_sprite.rect.center}')
                        if self.selected_tiles[1] == selected_sprite.tile_type \
                                and self.selected_tiles[0].rect.center != selected_sprite.rect.center:
                            selected_sprite.kill()
                            self.selected_tiles[0].kill()
                            self.selected_tiles = []
                            self.tile_select.play()
                        else:
                            self.selected_tiles = []
                            selected_sprite.image = selected_sprite.locked_image.copy()
                            for any_tile in tile_group:
                                any_tile.image = any_tile.locked_image.copy()

    def select_bad(self):
        self.empty_select.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
