# coding: utf-8
import sys
import pygame
from pygame.locals import *
from gamePackage.map.map import Map


class Game(object):
    __instance = None

    @staticmethod
    def get_instance(screen):
        if not Game.__instance:
            Game(screen)
        return Game.__instance

    def __init__(self, screen):
        # Screen used
        self.screen = screen
        # Frame rate (clock tick in the while true of the game)
        self.framerate = 60
        self.clock = pygame.time.Clock()
        # Map loaded in the game
        self.map = None
        # Set the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.static_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.ground_sprite = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.hole_sprites = pygame.sprite.Group()
        self.finish_sprite = pygame.sprite.Group()
        # Character of the player
        self.player = None
        # Tile height and Tile width
        self.tile_height = 32
        self.tile_width = 32
        # Select a font for the game
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        # When creating an instance start a new game
        self.new_game()

    def new_game(self):
        # Load the map
        self.map = Map(self, "../map/map_1.tmx")
        self.draw_static_sprites()
        # pygame.display.update()

        # Start the game
        self.__run_game()

    def __run_game(self):
        while True:
            # Tick for the framerate
            self.clock.tick(self.framerate)
            self.__events()
            # TODO : FIXME : Find out how this really works so it can be optimized (drawing updating etc.)
            self.draw()
            self.update()
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
        # FIXME : For now I draw the Ground sprite on each tick to override where the player image was
        self.ground_sprite.update()
        # Draw the player after all_sprites so it's displayed on top of the others
        self.player_sprite.update()
        pygame.display.update()

    def draw(self):
        """
        Draw all the sprites
        """

        # FIXME : For now I draw the Ground sprite on each tick to override where the player image was
        self.ground_sprite.draw(self.screen)
        # Draw the player after all_sprites so it's displayed on top of the others
        self.player_sprite.draw(self.screen)

    def draw_static_sprites(self):
        self.static_sprites.draw(self.screen)
        self.static_sprites.update(self.screen)

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        :return:
        """
        # It's ugly but it works !
        text = self.font.render("GAME OVER", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to continue", 1, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)

        self.reload_game()

    def reload_game(self):
        """
        Reload a new game on the same map
        Delete the old instance of the game and start a new one
        """
        screen = self.screen
        game = Game.get_instance(screen)
        del game
        Game.get_instance(screen)

    def load_next_map(self):
        text = self.font.render("GOOD JOB ", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to go to next level", 1, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)
        self.reload_game()
