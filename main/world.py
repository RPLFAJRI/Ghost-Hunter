import pickle
import pygame
from base import WorldObject
from enemies import Ghost

NUM_TILES = 60
TILE_SIZE = 16

_img_list: list = []
for _index in range(1, NUM_TILES + 1):
    _img = pygame.image.load(f'Tiles/{_index}.png')
    _img_list.append(_img)


class Ladder(WorldObject):
    pass


class Water(WorldObject):
    pass


class Diamond(WorldObject):
    pass


class Potion(WorldObject):
    pass


class Exit(WorldObject):
    def __init__(self, x: int, y: int, tile_data: tuple):
        super().__init__(x, y, tile_data)
        self.image = pygame.transform.scale(tile_data[0], (24, 24))
        self.rect.y = y - 8


class World:
    _GROUND_TILES = frozenset({0, 1, 2, 3, 4, 5, 6, 11})
    _ROCK_TILES   = frozenset({7, 14, 18, 19, 20, 21, 25, 26, 27, 28,
                                32, 33, 34, 35, 42, 43, 44, 45})
    _DECOR_TILES  = frozenset({8, 9, 10, 13, 15, 16, 17, 23, 24,
                                30, 31, 37, 38, 39, 40, 46, 47, 48, 49, 50, 51})
    _DIAMOND_TILES = frozenset({52, 53, 56, 57})
    _POTION_TILES  = frozenset({54, 55, 58, 59})

    def __init__(self, objects_group: list):
        self.objects_group = objects_group

        self.ground_list: list = []
        self.rock_list: list   = []
        self.decor_list: list  = []

    def generate_world(self, data: list, win: pygame.Surface) -> None:
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = _img_list[tile - 1]
                    rect = img.get_rect()
                    rect.x = x * TILE_SIZE
                    rect.y = y * TILE_SIZE
                    tile_data = (img, rect)

                    self._categorize_tile(tile, x, y, tile_data, win)

    def draw_world(self, win: pygame.Surface, screen_scroll: int) -> None:
        for tile_list in (self.ground_list, self.rock_list, self.decor_list):
            for tile in tile_list:
                tile[1][0] += screen_scroll
                win.blit(tile[0], tile[1])

    def _categorize_tile(self, tile: int, x: int, y: int,
                          tile_data: tuple, win: pygame.Surface) -> None:
        px, py = x * TILE_SIZE, y * TILE_SIZE

        if tile in self._GROUND_TILES:
            self.ground_list.append(tile_data)

        elif tile in self._ROCK_TILES:
            self.rock_list.append(tile_data)

        elif tile in self._DECOR_TILES:
            self.decor_list.append(tile_data)

        elif tile == 12:
            self.objects_group[4].add(Exit(px, py, tile_data))

        elif tile == 41:
            self.objects_group[0].add(Water(px, py, tile_data))

        elif tile in self._DIAMOND_TILES:
            self.objects_group[1].add(Diamond(px, py, tile_data))

        elif tile in self._POTION_TILES:
            self.objects_group[2].add(Potion(px, py, tile_data))

        elif tile == 60:
            self.objects_group[3].add(Ghost(px, py, win))


def load_level(level: int) -> tuple:
    file = f'Levels/level{level}_data'
    with open(file, 'rb') as f:
        data = pickle.load(f)
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] >= 0:
                data[y][x] += 1
    return data, len(data[0])
