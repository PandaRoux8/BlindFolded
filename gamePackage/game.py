# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import sys
import pygame
import constants


class AbstractGame:
    """
    Abstract class for the game with the base fields and the base function.
    """

    def __init__(self, screen):
        """
        :param screen:  pygame.Screen object
        """
        self.map = None  # .Map object -> This is where the current map of the game is stored
        self.blind = None  # .Blind object -> This is where the blind sprite is stored
        self._clock = pygame.time.Clock()  # Clock to set framerate later on
        self.screen = screen

        # Set sprites groups
        self.all_sprites = pygame.sprite.Group()
        self.static_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.kill_sprites = pygame.sprite.Group()
        self.finish_sprite = pygame.sprite.Group()
        self.teleporter_sprites = pygame.sprite.Group()
        self.blind_sprite = pygame.sprite.Group()

        self._load_map(screen)
        self._start_game()

    def _load_map(self, screen):
        """
        Abstract method to be implemented
        This method should load the map
        :param screen: pygame.Screen object
        """
        pass

    def _start_game(self):
        """
        Start the main loop of the game
        """
        # While true here and not in run game, so we can inherit run_game method and add stuff in the loop
        while True:
            self._run_game()

    def _run_game(self):
        """
        Run the main function for the game to work
        """
        self._check_exit_game()
        self._clock.tick(constants.FRAMERATE)
        self.map.draw()
        self.map.update()

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        """
        self.map.display_game_over()
        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self._clock.tick(constants.FRAMERATE)
        self.reload_game(from_game_over=True)

    def reload_game(self, from_game_over=False):
        """
        Abstract Method
        Reload a new game on the same map
        Delete the old instance of the game and start a new one
        :param from_game_over : from_game_over is True we load the current map, otherwise we load the next map
        """
        pass

    def next_level(self):
        """
        Display the end level message and reload the game with the next map
        """
        self.map.display_end_level_message()
        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self._clock.tick(constants.FRAMERATE)
        self.reload_game()

    def exit_game(self):
        """
        Exit the game
        """
        pygame.quit()
        sys.exit()

    def _check_exit_game(self):
        """
        Check if the player asked to exit the game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
