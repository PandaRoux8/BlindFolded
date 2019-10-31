# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

# coding: utf-8
import pygame


class Turret(pygame.sprite.Sprite):
    def __init__(self, game, tile, x, y, turret_shot_tile, axis_x=True):
        """
        :param game: Game object
        :param tile: image for the sprite
        :param x: position in x axis
        :param y: position in y axis
        :param turret_shot_tile: image for the turret shot
        :param axis_x: bool to know if the turret should shot in x or y axis
        """
        super(Turret, self).__init__()
        self.__game = game
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        game.static_sprites.add(self)
        game.all_sprites.add(self)
        self.display_shot(turret_shot_tile, axis_x)

    def display_shot(self, turret_shot_tile, shoot_in_x):
        """
        Display the shot of the turret on the map.
        :param turret_shot_tile: image of the turret shot
        """
        if shoot_in_x:
            new_image = pygame.transform.rotate(turret_shot_tile, 90)
            for i in range(0, self.rect.y, 32):
                values = {
                    'x': self.rect.x,
                    'y': i,
                    'tile': new_image
                }
                TurretShot(self.__game, values['tile'], values['x'], values['y'])
        else:
            for i in range(0, self.rect.y, 32):
                values = {
                    'x': self.rect.x,
                    'y': i,
                    'tile': turret_shot_tile
                }
                TurretShot(self.__game, values['tile'], values['x'], values['y'])


class TurretShot(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        """
        :param game: Game object
        :param tile: image for the sprite
        :param x: int for x axis position
        :param y: int for y axis position
        """
        super(TurretShot, self).__init__()
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        game.all_sprites.add(self)
        game.kill_sprites.add(self)
