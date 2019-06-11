# coding: utf-8
import pygame


class TeleporterManager(object):
    def __init__(self, ):
        self.blue_teleporter = []
        self.red_teleporter = []
        self.pink_teleporter = []

    def create_teleporter(self, game, tile, x, y, tile_index):
        res = Teleporter(game, tile, x, y)
        if tile_index == 4:
            if not self.blue_teleporter:
                self.blue_teleporter.append(res)
            else:
                self.blue_teleporter[0].destination_x = x
                self.blue_teleporter[0].destination_y = y
                res.destination_x = self.blue_teleporter[0].rect.x
                res.destination_y = self.blue_teleporter[0].rect.y
                self.blue_teleporter.append(res)
        elif tile_index == 5:
            if not self.red_teleporter:
                self.red_teleporter.append(res)
            else:
                self.red_teleporter[0].destination_x = x
                self.red_teleporter[0].destination_y = y
                res.destination_x = self.red_teleporter[0].rect.x
                res.destination_y = self.red_teleporter[0].rect.y
                self.red_teleporter.append(res)
        elif tile_index == 6:
            if not self.pink_teleporter:
                self.pink_teleporter.append(res)
            else:
                self.pink_teleporter[0].destination_x = x
                self.pink_teleporter[0].destination_y = y
                res.destination_x = self.pink_teleporter[0].rect.x
                res.destination_y = self.pink_teleporter[0].rect.y
                self.pink_teleporter.append(res)
        else:
            raise Exception("Error : This is not a teleporter tile")
        return res

    def check_teleporter(self):
        if len(self.blue_teleporter) % 2 != 0:
            raise Exception("One of the blue teleporter is alone.")
        if len(self.red_teleporter) % 2 != 0:
            raise Exception("One of the red teleporter is alone.")
        if len(self.pink_teleporter) % 2 != 0:
            raise Exception("One of the pink teleporter is alone.")


class Teleporter(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        super(Teleporter, self).__init__()
        self.__game = game
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.destination_x = None
        self.destination_y = None

        game.teleporter_sprites.add(self)
        game.static_sprites.add(self)
        game.all_sprites.add(self)
