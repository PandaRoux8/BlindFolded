import pygame
from gamePackage.map.map_parser import MapParser
from gamePackage.sprite.ground import Ground
from gamePackage.sprite.player import Player
from gamePackage.sprite.wall import Wall
from gamePackage.sprite.hole import Hole
from gamePackage.sprite.turret import Turret
from gamePackage.sprite.finish import Finish
from gamePackage.sprite.teleporter import TeleporterManager


class Map(object):
    def __init__(self, game, screen, map_file):
        self.map = MapParser(map_file)
        self.__game = game
        self.screen = screen
        # Select a font for the game
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        self.render_map()

    def render_map(self):
        tp_manager = TeleporterManager()
        for x, row in enumerate(self.map.map):
            for y, value in enumerate(row):
                values = {
                    'tile': self.map.tile[value - 1],  # value -1 because XML values start at 1 and the list of tiles start at 0
                    'x': x * 32,
                    'y': y * 32,
                }
                self.render_tiles(value-1, values, tp_manager)
        self.map_verification(tp_manager)

    def map_verification(self, tp_manager):
        """
        Do the required check for the map to be sure it's element are good.
        For example we check that there's a set of 2 telporter
        :param tp_manager: .TeleporteManager
        """
        tp_manager.check_teleporter()

    def render_tiles(self, tile_index, values, tp_manager):
        """
        Render the tiles. The tile index is defined by how the tile image is drawn.
        :param tile_index: int Tile index
        :param values: dict containing :
                        1. pygame.Surface the tile image
                        2. int The x position
                        3. int The y position
        :param tp_manager: TeleporterManager object
        :return: The object created
        """
        res = None
        if tile_index == 0:
            res = Wall(self.__game, values['tile'], values['x'], values['y'])
        elif tile_index == 1:
            res = Hole(self.__game, values['tile'], values['x'], values['y'])
        elif tile_index == 2:
            # Careful here is hardcode -> The shot sprite of the turret has to be the tile next to the turret
            # print("xx", self.map.tile[tile_index+1])
            res = Turret(self.__game, values['tile'], values['x'], values['y'], self.map.tile[tile_index+1], False)
        # Tile 3 is reserved for the turret shot
        elif tile_index == 4:
            tp_manager.create_teleporter(self.__game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 5:
            tp_manager.create_teleporter(self.__game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 6:
            tp_manager.create_teleporter(self.__game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 8:
            res = Ground(self.__game, values['tile'], values['x'], values['y'])
        elif tile_index == 9:
            res = Finish(self.__game, values['tile'], values['x'], values['y'])
        elif tile_index == 16:
            Player(self.__game, values['tile'], values['x'], values['y'])
            # Quick fix so the Player tile is replaced by a ground tile after he moves for the first time
            # TODO : Is this right ?
            values['tile'] = self.map.tile[8]
            res = self.render_tiles(8, values, tp_manager)
        return res

    def draw_static_sprites(self):
        self.__game.static_sprites.draw(self.screen)
        self.__game.static_sprites.update(self.screen)
        # Update the whole screen
        pygame.display.update()

    def update(self):
        """
        Update sprites
        """
        self.__game.player.update()
        # if self.__game.player:
        #     # pygame.display.update(self.__game.player.rect)
        #     x = self.__game.player.rect.x
        #     y = self.__game.player.rect.y
        #     rect_to_update = pygame.Rect(x-32, y-32, 96, 96)
        #
        #     pygame.display.update(rect_to_update)
            # self.__game.all_sprites.update()

        # self.__game.player_sprite.update()
        # self.__game.static_sprites.update()
        pygame.display.update()

    def draw(self):
        """
        Draw all the sprites
        """
        # FIXME : For now I draw the Ground sprite on each tick to override where the player image was
        #         (Only if the player moved)
        # if self.__game.player.has_moved:
        self.__game.all_sprites.draw(self.screen)
        self.__game.player.has_moved = False
        self.__game.player_sprite.draw(self.screen)

    def display_game_over(self):
        # TODO : It's ugly but it works !
        text = self.font.render("GAME OVER", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to continue", 1, (255, 255, 255))
        # TODO : More MVC ? It should be done in view (map)
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))

    def display_end_level_message(self):
        text = self.font.render("GOOD JOB ", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to go to next level", 1, (255, 255, 255))
        # TODO : More MVC ? It should be done in view (map)
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))
