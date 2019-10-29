# coding: utf-8
import pygame


class TeleporterManager(object):

    def __init__(self):
        self._blue_teleporter = []
        self._red_teleporter = []
        self._pink_teleporter = []

    def create_teleporter(self, game, tile, x, y, tile_index):
        """
        Create a telporter and add it on the map
        :param game: Game object
        :param tile: image for the sprite
        :param x: position in x axis
        :param y: position in y axis
        :param tile_index: int tile index (to know which telporter it is : blue, red or pink)
        :return Telporter object
        """
        teleporter = Teleporter(game, tile, x, y)
        if tile_index == 4:
            self.add_new_telporter(self._blue_teleporter, x, y, teleporter)
        elif tile_index == 5:
            self.add_new_telporter(self._red_teleporter, x, y, teleporter)
        elif tile_index == 6:
            self.add_new_telporter(self._pink_teleporter, x, y, teleporter)
        else:
            raise Exception("Error : This is not a teleporter tile")
        return teleporter

    def add_new_telporter(self, telporter_list, x, y, teleporter):
        """
        Add a new telporter on the map
        :param telporter_list: which telporter it is blue, red or pink
        :param x: position in x axis
        :param y: position in y axis
        :param teleporter: Teleporter object
        """
        if not telporter_list:
            telporter_list.append(teleporter)
        else:
            telporter_list[0].destination_x = x
            telporter_list[0].destination_y = y
            teleporter.destination_x = telporter_list[0].rect.x
            teleporter.destination_y = telporter_list[0].rect.y
            telporter_list.append(teleporter)

    def check_teleporter(self):
        """
        Check if we have a set of 2 telporter on the map.
        """
        if len(self._blue_teleporter) % 2 != 0:
            raise Exception("One of the blue teleporter is alone.")
        if len(self._red_teleporter) % 2 != 0:
            raise Exception("One of the red teleporter is alone.")
        if len(self._pink_teleporter) % 2 != 0:
            raise Exception("One of the pink teleporter is alone.")


class Teleporter(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        """
        :param game: Game object
        :param tile: image for the sprite
        :param x: int for x axis position
        :param y: int for y axis position
        """
        super(Teleporter, self).__init__()
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.destination_x = None
        self.destination_y = None

        game.teleporter_sprites.add(self)
        game.static_sprites.add(self)
        game.all_sprites.add(self)
