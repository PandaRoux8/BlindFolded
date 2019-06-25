# coding: utf-8
import pygame
from gamePackage.menu.main_menu import MainMenu
from gamePackage.game import Game


class Core(object):

    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Set title of the window
        pygame.display.set_caption('Blindfolded')
        # TODO : get this from a file
        # Screen size
        self.width = 832
        self.height = 832
        # Init the screen size
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Frame rate (clock tick in the while true of the game)
        self.framerate = 15
        self.clock = pygame.time.Clock()

        # Save the main menu instance
        self.main_menu = None
        # Save game instance
        self.game = None
        self.start_app()

    def start_app(self):
        self.call_main_menu()

    def call_main_menu(self):
        if not self.main_menu:
            self.main_menu = MainMenu(self.screen, (self.width, self.height), self)
        else:
            self.main_menu.enable()

    def call_option_menu(self):
        pass

    def call_ingame_menu(self):
        pass

    def call_lobby(self):
        pass

    def start_player_game(self):
        # Todo : Check if 2 player are connected
        self.game = Game()

    def start_observer_game(self):
        pass
