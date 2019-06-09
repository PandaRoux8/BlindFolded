# coding: utf-8
import pygame


class Turret(pygame.sprite.Sprite):
    def __init__(self, game, tile, x, y, turret_shot_tile, axis_x=True):
        super(Turret, self).__init__()
        self.__game = game
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Select if the turret shoot in x axis or y axis
        self.shoot_in_x = axis_x
        self.display_shot(turret_shot_tile)

    def display_shot(self, turret_shot_tile):
        if not self.shoot_in_x:
            for i in range(0, self.rect.y, 32):
                values = {
                    'x': self.rect.x,
                    'y': i,
                    'tile': turret_shot_tile
                }
                turret_shot = TurretShot(values['tile'], values['x'], values['y'])
                self.__game.all_sprites.add(turret_shot)
                self.__game.hole_sprites.add(turret_shot)
        else:
            new_image = pygame.transform.rotate(turret_shot_tile, 90)
            for i in range(0, self.rect.y, 32):
                values = {
                    'x': self.rect.x,
                    'y': i,
                    'tile': new_image
                }
                turret_shot = TurretShot(values['tile'], values['x'], values['y'])
                self.__game.all_sprites.add(turret_shot)
                self.__game.hole_sprites.add(turret_shot)


class TurretShot(pygame.sprite.Sprite):

    def __init__(self, tile, x, y):
        super(TurretShot, self).__init__()
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y