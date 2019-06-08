# coding: utf-8
from gamePackage.map.map_parser import MapParser
from gamePackage.sprite.ground import Ground
from gamePackage.sprite.player import Player
from gamePackage.sprite.wall import Wall
from gamePackage.sprite.hole import Hole
from gamePackage.sprite.turret import Turret
from gamePackage.sprite.finish import Finish


class Map(object):
    def __init__(self, game, map_file):
        self.map = MapParser(map_file)
        self.__game = game
        self.render_map()

    def render_map(self):
        for x, row in enumerate(self.map.map):
            for y, col in enumerate(row):
                values = {
                    'tile': self.map.tile[col - 1],
                    'x': x * 32,
                    'y': y * 32,
                }
                self.render_tiles(col-1, values)

    def render_tiles(self, tile_index, values):
        """
        Render the tiles. The tile index is defined by how the tile image is drawn.
        :param tile_index: int Tile index
        :param values: dict containing :
                        1. pygame.Surface the tile image
                        2. int The x position
                        3. int The y position
        :return: The object created
        """
        res = None
        if tile_index == 0:
            res = Wall(self.__game, values['tile'], values['x'], values['y'])
            # TODO : Place these in the linked class
            self.__game.wall_sprites.add(res)
            self.__game.static_sprites.add(res)
            self.__game.all_sprites.add(res)
        elif tile_index == 1:
            res = Hole(self.__game, values['tile'], values['x'], values['y'])
            # TODO : Place these in the linked class
            self.__game.hole_sprites.add(res)
            self.__game.static_sprites.add(res)
            self.__game.all_sprites.add(res)
        elif tile_index == 2:
            # Careful here is hardcode -> The shot sprite of the turret has to be the tile next to the turret
            # print("xx", self.map.tile[tile_index+1])
            res = Turret(self.__game, values['tile'], values['x'], values['y'], self.map.tile[tile_index+1])
            # TODO : Place these in the linked class
            self.__game.static_sprites.add(res)
            self.__game.all_sprites.add(res)
        elif tile_index == 8:
            res = Ground(self.__game, values['tile'], values['x'], values['y'])
            # TODO : Place these in the linked class
            self.__game.ground_sprite.add(res)
            self.__game.static_sprites.add(res)
            self.__game.all_sprites.add(res)
        elif tile_index == 9:
            res = Finish(self.__game, values['tile'], values['x'], values['y'])
            self.__game.static_sprites.add(res)
            self.__game.all_sprites.add(res)
            self.__game.finish_sprite.add(res)
        elif tile_index == 16:
            res = Player(self.__game, values['tile'], values['x'], values['y'])
            self.__game.player_sprite.add(res)
            res.walls = self.__game.wall_sprites
            res.holes = self.__game.hole_sprites
            res.finish_tile = self.__game.finish_sprite

            # Quick fix so the Player tile is replaced by a ground tile after he moves for the first time
            # TODO : Is this right ?
            values['tile'] = self.map.tile[8]
            res = self.render_tiles(8, values)
        return res
