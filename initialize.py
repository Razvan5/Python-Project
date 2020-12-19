import numpy
import random


class Initialize:
    """
    Class used for easy level creation, working for any zoom level as long as the screen is big enough; the constructor
    has a counter, an empty dictionary and a list with all the tiles type. It can hold up to a maximum of 152 tiles!\n
    :param mahjong_dictionary: empty or partially filled dictionary
    :type: dict
    """
    def __init__(self, mahjong_dictionary):
        self.mahjong = mahjong_dictionary
        self.index = 1
        self.tile_types_range = list(range(1, 38)) * 4
        random.shuffle(self.tile_types_range)

    def draw_line(self, start, end, static_coord, layer_height, orientation):
        """
        Draws a line of tiles equally distanced apart, between start and end, at a fixed coordinate with the option of
        changing the direction and layer height\n
        :param start: a float number that can take any value
        :type start: float
        :param end: a float number that can only take values equal to start+2n
        :type end: float
        :param static_coord: the fixed coordinate for the line to appear at
        :type static_coord: float
        :param layer_height: the height of the tile line, the bigger the number the higher the line; affects
            interactions
        :type layer_height: int
        :param orientation: can either be vertical or horizontal, any other value will return an unmodified dictionary
        :type orientation: str
        :return: the modified dictionary that can be represented as a line of tiles
        :rtype: dict
        """

        if orientation == 'horizontal':
            for x in numpy.arange(start, end, 2):
                self.mahjong.update({self.index: (layer_height, x, static_coord, self.tile_types_range.pop())})
                self.index += 1
        elif orientation == 'vertical':
            # -3.5 min,2 step ,8.5 max
            for y in numpy.arange(start, end, 2):
                self.mahjong.update({self.index: (layer_height, static_coord, y, self.tile_types_range.pop())})
                self.index += 1
        else:
            print("Un-existing Orientation...Returning dictionary!")

        return self.mahjong

    def draw_piece(self, coord_x, coord_y, layer_height):
        """
        Draws a tile at a specific x and y and height\n
        :param coord_x: the middle x coordinate of the tile, recommended between -13 and 14
        :type coord_x: float
        :param coord_y: the middle x coordinate of the tile, recommended values between -3.5 and 8.5
        :type coord_y: float
        :param layer_height: used for determining if a tile is over, under or around another tile
        :type layer_height: int
        :return: updates the dictionary
        """

        self.mahjong.update({self.index: (layer_height, coord_x, coord_y, self.tile_types_range.pop())})
        self.index += 1
