import pygame
from pygame.locals import *
from gamePackage.menu.ingame_menu import InGameMenu
from gamePackage.network.client import Client

ALLOW_MOVE = pygame.USEREVENT + 1


class Player(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        super(Player, self).__init__()
        self.__game = game

        # Color of the Player
        self.image = tile
        # Position of the character in the grid (and his size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self._direction = 'up'
        # Speed of the Player
        self.speed = 32

        # Vector for moving the Player
        self.vx, self.vy = 0, 0

        self.has_moved = True
        self.allow_move = True

        game.player = self
        game.player_sprite.add(self)

    # @property
    # def direction(self):
    #     return self._direction
    #
    # @direction.setter
    # def direction(self, value):
    #     if self._direction != value:
    #         self._direction = value
    #         self.change_direction()
    #
    # def change_direction(self):
    #     self.image = pygame.transform.flip(self.image, False, True)

    def move_player(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if self.__game.guide:
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
        # if keys[pygame.K_f]:
        #     # Check surrounding
        #     self.check_surrounding()

        # Go to escape menu
        if keys[pygame.K_ESCAPE]:
            menu = InGameMenu.get_instance(self.__game.screen, (1600, 900))
            menu.display_menu()

        # # Set the speed at 3/4 than the usual when using 2 direction at the same time
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.5
        #     self.vy *= 0.5

    # def check_surrounding(self):
    #     for npc in self.__game.:
    #         if npc.rect.x == self.rect.x or npc.rect.y == self.rect.y:
    #             npc.talk()

    def update_position(self, pos_x, pos_y):
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        """
        Update the character position
        """
        self.move_player()
        self.rect.x += self.vx
        self.__game.collide_with_walls('x')
        self.rect.y += self.vy
        self.__game.collide_with_walls('y')
        self.__game.kill_on_collide()
        self.__game.teleport_player()
        self.__game.finish_map()
        if not self.__game.guide:
            Client.send_player_data(self.rect.x, self.rect.y)

    def check_exit_game(self):
        for event in pygame.event.get():
            if event.type == ALLOW_MOVE:
                self.allow_move = True
            if event.type == QUIT:
                self.__game.exit_game()
