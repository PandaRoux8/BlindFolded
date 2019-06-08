# coding: utf-8
import pygame
from gamePackage.menu.ingame_menu import InGameMenu


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
        self._direction = 'up'
        # Speed of the Player
        self.speed = 8

        # Vector for moving the Player
        self.vx, self.vy = 0, 0
        self.walls = None
        self.holes = None
        self.finish_tile = None

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if self._direction != value:
            self._direction = value
            self.change_direction()

    def change_direction(self):
        self.image = pygame.transform.flip(self.image, False, True)

    def move_player(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        # Up
        if keys[pygame.K_w]:
            self.vy = -self.speed
            self.direction = 'up'
        # Down
        if keys[pygame.K_s]:
            self.vy = self.speed
            self.direction = 'down'
        # Left
        if keys[pygame.K_a]:
            self.vx = -self.speed
            self.direction = 'left'

        # Right
        if keys[pygame.K_d]:
            self.vx = self.speed
            self.direction = 'right'

        if keys[pygame.K_f]:
            # Check surrounding
            self.check_surrounding()
            # if pnj -> Talk

        # Go to escape menu
        if keys[pygame.K_ESCAPE]:
            menu = InGameMenu.get_instance(self.__game.screen, (1600, 900))
            menu.display_menu()

        # Set the speed at 3/4 than the usual when using 2 direction at the same time
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.75
            self.vy *= 0.75

    def check_surrounding(self):
        for npc in self.__game.map.npcs:
            if npc.rect.x == self.rect.x or npc.rect.y == self.rect.y:
                npc.talk()

    def collide_with_walls(self, axis=None):
        """
        Check if the Character collide with any wall.
        Block the character in front of the wall if it's the case.
        Do it with x or y axis because if we do both at one time it does strange things. (ie the Player teleport)
        """
        # print("a", self, self.walls)
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, dokill=False)
        for block in block_hit_list:
            if axis == 'x':
                if self.vx > 0:
                    self.rect.right = block.rect.left
                else:
                    self.rect.left = block.rect.right

            if axis == 'y':
                if self.vy > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

    def fall_in_hole(self):
        """
        Check if the player has fallen into a hole
        """
        block_hit_list = pygame.sprite.spritecollide(self, self.holes, dokill=False)
        for block in block_hit_list:
            self.__game.game_over()

    def finish_map(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.finish_tile, dokill=False)
        for block in block_hit_list:
            self.__game.load_next_map()

    def update(self):
        """
        Update the character position
        """
        self.move_player()
        self.rect.x += self.vx
        self.collide_with_walls('x')
        self.rect.y += self.vy
        self.collide_with_walls('y')
        self.fall_in_hole()
        self.finish_map()
