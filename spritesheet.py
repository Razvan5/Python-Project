import pygame
import tile

class SpriteSheet(pygame.sprite.Sprite):

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        try:
            self.sprite_sheet = pygame.image.load(filepath).convert()
            self.overlay = pygame.image.load("images/others/tile_select.png")
        except pygame.error as sprite_load_error:
            print(f"Unable to load sprite sheet image:{filepath}")
            raise SystemExit(sprite_load_error)
        self.select = False

    def sprite_at(self, sprite_sheet_x, sprite_sheet_y, width, height, on_table_x, on_table_y, layer, tile_type):
        self.image = pygame.Surface((width, height))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.sprite_sheet, (0, 0), pygame.Rect(sprite_sheet_x, sprite_sheet_y, width, height))
        self.rect = self.image.get_rect()
        self.rect.center = [on_table_x, on_table_y]
        # TODO : remove prints from all classes and make the
        new_tile = tile.Tile(self.image, self.rect, self.rect.center, layer, tile_type)
        return new_tile

    def all_sprites(self, mahjong_vertex_dictionary, width, height, middle_x, middle_y):
        return [
            [self.sprite_at(1+110*sprite_type, 1, width, height, middle_x+width/2*x, middle_y+height/2*y, layer,
                            sprite_type),
             middle_x+width/2*x, middle_y+height/2*y]
            for layer, x, y, sprite_type in mahjong_vertex_dictionary.values()]

    def select_tile(self):
        self.select = True
        self.image.blit(self.overlay, (0, 0), pygame.Rect(0, 0, 108, 140))
