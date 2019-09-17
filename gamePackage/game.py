import sys
import pygame
from gamePackage.map.map import Map


class Game(object):

    def __init__(self, screen):
        # Map loaded in the game
        self.map = None
        # Character of the player
        self.blind = None

        # TODO : Get these from __main__ ? Or from a file ?
        # Game clock
        self.clock = pygame.time.Clock()
        self.framerate = 15

        # Set the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.static_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.kill_sprites = pygame.sprite.Group()
        self.finish_sprite = pygame.sprite.Group()
        self.teleporter_sprites = pygame.sprite.Group()
        self.blind_sprite = pygame.sprite.Group()

        self.load_map(screen)
        # self.start_game()
        # self.run_game()

    def load_map(self, screen):
        self.start_game()

    def start_game(self):
        while True:
            self.run_game()

    def run_game(self):
        self.clock.tick(self.framerate)
        self.blind.check_exit_game()
        # Tick for the framerate
        # TODO : FIXME : Find out how this really works so it can be optimized (drawing updating etc.)
        self.map.draw()
        self.map.update()

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        :return:
        """
        self.map.display_game_over()

        # TODO : More MVC ? Place it on the controller
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
        pass

    def load_next_map(self):
        self.map.display_end_level_message()
        self.search_map()

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)
        self.reload_game()

    def exit_game(self):
        pygame.quit()
        sys.exit()
