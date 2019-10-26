import pygame
from pygame.locals import *
from gamePackage.menu.ingame_menu import InGameMenu

ALLOW_MOVE = pygame.USEREVENT + 1


class Blind(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        super(Blind, self).__init__()
        self._game = game

        # Color of the blind
        self.image = tile
        # Position of the character in the grid (and his size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self._direction = 'up'
        # Speed of the blind
        self.speed = 32

        # Vector for moving the blind
        self.vx, self.vy = 0, 0

        self.has_moved = True
        self.allow_move = True

        game.blind = self
        game.blind_sprite.add(self)

    def move_blind(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if type(self._game).__name__ == "GameBlind":
            # Up
            if keys[pygame.K_w] and self.allow_move:
                self.vy = -self.speed
                # self.direction = 'up'
                self.has_moved = True
            # Down
            if keys[pygame.K_s] and self.allow_move:
                self.vy = self.speed
                # self.direction = 'down'
                self.has_moved = True
            # Left
            if keys[pygame.K_a] and self.allow_move:
                self.vx = -self.speed
                # self.direction = 'left'
                self.has_moved = True
            # Right
            if keys[pygame.K_d] and self.allow_move:
                self.vx = self.speed
                # self.direction = 'right'
                self.has_moved = True

            if self.has_moved:
                self.allow_move = False
                pygame.time.set_timer(ALLOW_MOVE, 100)

        # Go to escape menu
        if keys[pygame.K_ESCAPE]:
            menu = InGameMenu.get_instance(self._game.screen, (1600, 900))
            menu.display_menu()

    def update_position(self, pos_x, pos_y):
        print("UP", pos_x, pos_y)
        self.rect.x = int(pos_x)
        self.rect.y = int(pos_y)

    def update(self):
        """
        Update the character position
        """
        if type(self._game).__name__ == "GameBlind":
            self.move_blind()
            self.rect.x += self.vx
            self._game.check_collision_with_walls('x')
            self.rect.y += self.vy
            self._game.check_collision_with_walls('y')
            self._game.check_collision_with_kill_sprite()
            self._game.check_collision_teleporter()
            self._game.check_end_level()
            if self.has_moved:
                self._game.client.send_blind_data(self.rect.x, self.rect.y)
            self.check_allow_move()

    def check_allow_move(self):
        for event in pygame.event.get():
            if event.type == ALLOW_MOVE:
                self.allow_move = True
