# coding: utf-8
import pygame


class Hole(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        super(Hole, self).__init__()
        self.__game = game
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Add to sprites group
        game.kill_sprites.add(self)
        game.static_sprites.add(self)
        game.all_sprites.add(self)
