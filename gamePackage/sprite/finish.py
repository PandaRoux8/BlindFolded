# coding: utf-8
import pygame


class Finish(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        """
        :param game: Game object
        :param tile: image for the sprite
        :param x: int for x axis position
        :param y: int for y axis position
        """
        super(Finish, self).__init__()
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        game.static_sprites.add(self)
        game.all_sprites.add(self)
        game.finish_sprite.add(self)
