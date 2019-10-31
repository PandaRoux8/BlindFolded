# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import pygame
import constants
from map.map_parser import MapParser
from sprite.ground import Ground
from sprite.blind import Blind
from sprite.wall import Wall
from sprite.hole import Hole
from sprite.turret import Turret
from sprite.finish import Finish
from sprite.teleporter import TeleporterManager


class Map(object):
    def __init__(self, game, screen, map_file, map_timer, blind=False):
        """
        :param game: Game object
        :param screen: pygame.Screen object
        :param map_file: string path for the map
        :param map_timer: string timer of the map
        """
        map_parser = MapParser(map_file, blind)
        self.array_map = map_parser.array_map
        self.tiles = map_parser.tile

        # Timer for the map
        self._timer = int(map_timer)
        self._clock = pygame.time.Clock()
        self._delta_time = 0
        self.timer_done = False

        self._game = game
        self.screen = screen
        self.render_map()

    def render_map(self):
        """
        Parse the 2 dimension array given by map parser.
        Render the map using the id in the map array.
        """
        tp_manager = TeleporterManager()
        for x, row in enumerate(self.array_map):
            for y, value in enumerate(row):
                values = {
                    'tile': self.tiles[value - 1],  # value -1 because XML values start at 1 and the list of tiles start at 0
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
        Render the tiles. Using the tile_index we know which image we need to give
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
            res = Wall(self._game, values['tile'], values['x'], values['y'])
        elif tile_index == 1:
            res = Hole(self._game, values['tile'], values['x'], values['y'])
        elif tile_index == 2:
            # Careful here is hardcode -> The shot sprite of the turret has to be the tile next to the turret
            res = Turret(self._game, values['tile'], values['x'], values['y'], self.tiles[tile_index + 1], False)
        # Tile 3 is reserved for the turret shot
        elif tile_index == 4:
            tp_manager.create_teleporter(self._game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 5:
            tp_manager.create_teleporter(self._game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 6:
            tp_manager.create_teleporter(self._game, values['tile'], values['x'], values['y'], tile_index)
        elif tile_index == 8:
            res = Ground(self._game, values['tile'], values['x'], values['y'])
        elif tile_index == 9:
            res = Finish(self._game, values['tile'], values['x'], values['y'])
        elif tile_index == 16:
            Blind(self._game, values['tile'], values['x'], values['y'])
            # Quick fix so the blind tile is replaced by a ground tile after he moves for the first time
            values['tile'] = self.tiles[8]
            res = self.render_tiles(8, values, tp_manager)
        return res

    def draw_static_sprites(self):
        """
        Draw the static sprites on the screen
        """
        self._game.static_sprites.draw(self.screen)
        self._game.static_sprites.update(self.screen)
        # Update the whole screen
        pygame.display.update()

    def update(self):
        """
        Update sprites
        """
        self._game.blind.update()
        self.display_timer()
        pygame.display.update()

    def draw(self):
        """
        Draw all the sprites on the screen
        """
        # FIXME : For now I draw the Ground sprite on each tick to override where the blind image was
        #         (Only if the blind moved)
        # if self.__game.blind.has_moved:
        self._game.all_sprites.draw(self.screen)
        self._game.blind.has_moved = False
        self._game.blind_sprite.draw(self.screen)

    def display_game_over(self):
        """
        Display game over message on the screen
        """
        self.display_message("GAME OVER", "Press Space to continue")

    def display_end_level_message(self):
        """
        Display end level message on the screen
        """
        self.display_message("GOOD JOB", "Press Space to go to next level")

    def display_message(self, text1, text2):
        """
        Display a message on the screen
        :param text1: Main text to write
        :param text2: Second text to write
        """
        # TODO : This is ugly
        font1 = pygame.font.SysFont(constants.FONT, 50)
        font2 = pygame.font.SysFont(constants.FONT, 16)
        displayed_text1 = font1.render(text1, 1, constants.FONT_COLOR)
        displayed_text2 = font2.render(text2, 1, constants.FONT_COLOR)
        self.screen.blit(displayed_text1, (constants.WIDTH / 2 - 95, constants.HEIGHT / 2))
        self.screen.blit(displayed_text2, (constants.WIDTH / 2 - 95, constants.HEIGHT / 2 + 32))

    def display_timer(self):
        """
        Display the timer on the screen
        """
        self._timer -= self._delta_time
        if self._timer <= 0:
            self.timer_done = True
        self._delta_time = self._clock.tick(30) / 1000

        font = pygame.font.SysFont(constants.FONT, 40)
        text = font.render(str(int(self._timer)), 1, constants.FONT_COLOR)
        self.screen.blit(text, (32, 32))
