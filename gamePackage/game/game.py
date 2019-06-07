# coding: utf-8
import sys
import pygame
from pygame.locals import *
from gamePackage.map.map import Map


# TODO make this a singleton ?
class Game(object):

    def __init__(self, screen):
        # Screen used
        self.screen = screen
        # Frame rate (clock tick in the while true of the game)
        self.framerate = 60
        self.clock = pygame.time.Clock()
        # Map loaded in the game
        self.map = None
        # Sprite linked in the game
        self.all_sprites = None
        self.player_sprite = None
        self.ground_sprite = None
        self.wall_sprites = None
        self.npc_sprites = None
        self.hole_sprites = None
        # Character of the player
        self.player = None
        # Tile height and Tile width
        self.tile_height = 32
        self.tile_width = 32
        # Select a font for the game
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        print(self.font)
        # When creating an instance start a new game
        self.new_game()

    def new_game(self):
        # Set the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.ground_sprite = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.hole_sprites = pygame.sprite.Group()

        # Load the map
        self.map = Map(self, "../map/map_1.tmx")

        # # Static init of a NPC -> Dynamic NPC from map
        # npc = NPC(self, 128, 128)
        # self.wall_sprites.add(npc)
        # self.all_sprites.add(npc)
        #
        #
        # # Load the character
        # self.player = Charachter(self, 64, 64)
        # # Add walls to the character (?)
        # self.player.walls = self.wall_sprites
        # self.player_sprite.add(self.player)
        # self.all_sprites.add(self.player)

        # Start the game
        self.__run_game()

    def __run_game(self):
        while True:
            # Tick for the framerate
            self.clock.tick(self.framerate)
            self.__events()
            self.update()
            self.draw()
            # pygame.display.update()

    def __events(self):
        """
        Catch leave events
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        """
        Update all the sprites
        """
        self.all_sprites.update()

    def draw(self):
        """
        Draw all the sprites
        """
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        :return:
        """
