# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import pygame
from game import AbstractGame
from map.map import Map
from menu.pause_menu import PauseMenu


class GameGuide(AbstractGame):

    def __init__(self, screen, server):
        self.server = server
        super(GameGuide, self).__init__(screen)

    def _load_map(self, screen):
        """
        Load the map
        :param screen: pygame.Screen object
        """
        # Wait for map to be loaded on blind and sent here
        while not self.server.map:
            self.server.listen()
        map_path = self.server.map
        # Load the map
        self.map = Map(self, screen, map_path, self.server.map_timer)
        self.map.draw_static_sprites()
        super(GameGuide, self)._load_map(screen)

    def _run_game(self):
        """
        Inherit run game to add the listening for the server on each iteration
        """
        super(GameGuide, self)._run_game()
        if self.server:
            if not self.server.blind:
                self.server.blind = self.blind
            if not self.server.game:
                self.server.game = self
            self.server.listen()
            self._check_keys()

    def _check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.server.send_pause_game()
            PauseMenu(self.screen)
            self.server.check_client_ready()

    def reload_game(self, from_game_over=False):
        """
        Reload a new game
        Delete the old instance of the game and start a new one
        from_game_over : from_game_over is True we load the current map, otherwise we load the next map
        """
        # Wait for the blind to be ready
        self.server.check_client_ready()
        screen = self.map.screen
        self.server.map = False  # Reset the map so we always get the one from the blind
        server = self.server
        del self
        GameGuide(screen, server)

    def pause_game(self):
        PauseMenu(self.screen)
        self.server.check_client_ready()

    def exit_game(self):
        self.server.release()
        super(GameGuide, self).exit_game()

