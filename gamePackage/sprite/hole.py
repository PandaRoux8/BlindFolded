# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

# coding: utf-8
import pygame


class Hole(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        """
        :param game: Game object
        :param tile: image for the sprite
        :param x: int for x axis position
        :param y: int for y axis position
        """
        super(Hole, self).__init__()
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Add to sprites group
        game.kill_sprites.add(self)
        game.static_sprites.add(self)
        game.all_sprites.add(self)
