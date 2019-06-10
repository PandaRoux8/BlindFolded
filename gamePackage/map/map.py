# coding: utf-8
import pygame
from gamePackage.map.map_parser import MapParser
from gamePackage.sprite.ground import Ground
from gamePackage.sprite.player import Player
from gamePackage.sprite.wall import Wall
from gamePackage.sprite.hole import Hole
from gamePackage.sprite.turret import Turret
from gamePackage.sprite.finish import Finish
from gamePackage.sprite.teleporter import TeleporterManager, Teleporter


class Map(object):
    def __init__(self, game, map_file):
        self.map = MapParser(map_file)
        self.game = game
        self.render_map()

    def render_map(self):
        tp_manager = TeleporterManager()
        for x, row in enumerate(self.map.map):
            for y, col in enumerate(row):
                values = {
                    'tile': self.map.tile[col - 1],
                    'x': x * 32,
                    'y': y * 32,
                }
                self.render_tiles(col-1, values, tp_manager)
        self.map_verification(tp_manager)

    def map_verification(self, tp_manager):
        tp_manager.check_teleporter()

    def render_tiles(self, tile_index, values, tp_manager):
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
            res = Wall(self.game, values['tile'], values['x'], values['y'])
        elif tile_index == 1:
            res = Hole(self.game, values['tile'], values['x'], values['y'])
        elif tile_index == 2:
            # Careful here is hardcode -> The shot sprite of the turret has to be the tile next to the turret
            # print("xx", self.map.tile[tile_index+1])
            res = Turret(self.game, values['tile'], values['x'], values['y'], self.map.tile[tile_index+1], False)
        # Tile 3 is reserved for the turret shot
        elif tile_index == 4:
            tp_manager.create_teleporter(self.game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 5:
            tp_manager.create_teleporter(self.game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 6:
            tp_manager.create_teleporter(self.game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 8:
            res = Ground(self.game, values['tile'], values['x'], values['y'])
        elif tile_index == 9:
            res = Finish(self.game, values['tile'], values['x'], values['y'])
        elif tile_index == 16:
            Player(self.game, values['tile'], values['x'], values['y'])
            # Quick fix so the Player tile is replaced by a ground tile after he moves for the first time
            # TODO : Is this right ?
            values['tile'] = self.map.tile[8]
            res = self.render_tiles(8, values, tp_manager)
        return res

    def draw_static_sprites(self):
        self.game.static_sprites.draw(self.game.screen)
        self.game.static_sprites.update(self.game.screen)

    def update(self):
        """
        Update all the sprites
        """
        self.game.player_sprite.update()
        pygame.display.update()

    def draw(self):
        """
        Draw all the sprites
        """
        # FIXME : For now I draw the Ground sprite on each tick to override where the player image was
        #         (Only if the player moved)
        if self.game.player.has_moved:
            self.game.all_sprites.draw(self.game.screen)
            self.game.player.has_moved = False
        self.game.player_sprite.draw(self.game.screen)
