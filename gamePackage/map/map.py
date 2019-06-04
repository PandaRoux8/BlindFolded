# coding: utf-8
from gamePackage.map.map_parser import MapParser
from gamePackage.sprite.ground import Ground
from gamePackage.sprite.npc import NPC
from gamePackage.sprite.player import Player
from gamePackage.sprite.wall import Wall
from gamePackage.sprite.hole import Hole


class Map(object):
    def __init__(self, game, map_file):
        self.map = MapParser(map_file)
        self.__game = game
        self.npcs = []
        self.render_map()

    def render_map(self):
        player_values = {}
        for x, row in enumerate(self.map.map):
            for y, col in enumerate(row):
                # Hardcode -> 2nd tile in the tilset are the walls
                if col-1 == 0:
                    wall_values = {
                        'tile': self.map.tile[col-1],
                        'x': x*32,
                        'y': y*32,
                    }
                    self.render_wall(wall_values)
                if col-1 == 1:
                    hole_values = {
                        'tile': self.map.tile[col-1],
                        'x': x*32,
                        'y': y*32,
                    }
                    self.render_hole(hole_values)

                # Hardcode -> 16 tiles is the character sprite
                if col-1 == 16:
                    player_values = {
                        'tile': self.map.tile[col-1],
                        'x': x*32,
                        'y': y*32,
                    }
                    self.render_ground(player_values)
                # Harcode -> 17 tiles is the NPC sprite
                if col-1 == 17:
                    npc_values = {
                        'tile': self.map.tile[col-1],
                        'x': x*32,
                        'y': y*32,
                    }
                    self.render_npc(npc_values)
                # Other tiles are the ground
                else:
                    ground_values = {
                        'tile': self.map.tile[col-1],
                        'x': x*32,
                        'y': y*32,
                    }
                    self.render_ground(ground_values)

        if player_values:
            self.render_player(player_values)

    def render_ground(self, values):
        ground = Ground(self.__game, values['tile'], values['x'], values['y'])
        self.__game.ground_sprite.add(ground)
        self.__game.all_sprites.add(ground)

    def render_wall(self, values):
        wall = Wall(self.__game, values['tile'], values['x'], values['y'])
        self.__game.wall_sprites.add(wall)
        self.__game.all_sprites.add(wall)

    def render_hole(self, values):
        hole = Hole(self.__game, values['tile'], values['x'], values['y'])
        self.__game.all_sprites.add(hole)
        self.__game.hole_sprites.add(hole)

    def render_npc(self, values):
        npc = NPC(self.__game, values['tile'], values['x'], values['y'])
        self.npcs.append(npc)
        self.__game.all_sprites.add(npc)
        self.__game.wall_sprites.add(npc)
        self.__game.npc_sprites.add(npc)

    def render_player(self, values):
        player = Player(self.__game, values['tile'], values['x'], values['y'])
        self.__game.all_sprites.add(player)
        self.__game.player_sprite.add(player)
        player.walls = self.__game.wall_sprites
        player.holes = self.__game.hole_sprites
