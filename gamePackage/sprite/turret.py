# coding: utf-8
import pygame


class Turret(pygame.sprite.Sprite):
    def __init__(self, game, tile, x, y):
        super(Turret, self).__init__()
        self.__game = game
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.shoot_direction = None

    def shot(self):
        pass
