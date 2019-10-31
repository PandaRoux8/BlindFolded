# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import pygame
from menu.pause_menu import PauseMenu

ALLOW_MOVE = pygame.USEREVENT + 1


class Blind(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        """
        :param game: Game object
        :param tile: image for the sprite
        :param x: int for x axis position
        :param y: int for y axis position
        """
        super(Blind, self).__init__()
        self.__game = game
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Speed of the blind
        self._speed = 32
        # Vector to move the blind
        self.vx, self.vy = 0, 0

        self.has_moved = True
        self._allow_move = True

        game.blind = self
        game.blind_sprite.add(self)

    def move_blind(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if type(self.__game).__name__ == "GameBlind":
            # Up
            if keys[pygame.K_w] and self._allow_move:
                self.vy = -self._speed
                self.has_moved = True
            # Down
            if keys[pygame.K_s] and self._allow_move:
                self.vy = self._speed
                self.has_moved = True
            # Left
            if keys[pygame.K_a] and self._allow_move:
                self.vx = -self._speed
                self.has_moved = True
            # Right
            if keys[pygame.K_d] and self._allow_move:
                self.vx = self._speed
                self.has_moved = True

            if self.has_moved:
                self._allow_move = False
                pygame.time.set_timer(ALLOW_MOVE, 100)

        if keys[pygame.K_ESCAPE]:
            # TODO : We have to put this in the game part
            if type(self.__game).__name__ == "GameBlind":
                self.__game.client.send_pause_game()
                PauseMenu(self.__game.screen)
                self.__game.client.check_server_ready()

    def update_position(self, pos_x, pos_y):
        """
        Update the position of the blind.
        This one is called through the Server only
        :param pos_x: int x axis position
        :param pos_y: int y axis position
        """
        # TODO : Move this code so it's only accessible by the Guide
        self.rect.x = int(pos_x)
        self.rect.y = int(pos_y)

    def update(self):
        """
        To update the blind data we have to read the user input and proceed to some collision check.
        This method is called through the blind player only
        """
        # TODO : Move this code so it's only accessible by the Blind
        if type(self.__game).__name__ == "GameBlind":
            self.move_blind()
            self.rect.x += self.vx
            self.__game.check_collision_with_walls('x')
            self.rect.y += self.vy
            self.__game.check_collision_with_walls('y')
            self.__game.check_collision_with_kill_sprite()
            self.__game.check_collision_teleporter()
            self.__game.check_end_level()
            if self.has_moved:
                self.__game.client.send_blind_data(self.rect.x, self.rect.y)
            self.check_allow_move()

    def check_allow_move(self):
        """
        Check if the blind is allowed to move
        """
        for event in pygame.event.get():
            if event.type == ALLOW_MOVE:
                self._allow_move = True
