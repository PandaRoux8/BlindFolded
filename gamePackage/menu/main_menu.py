# coding: utf-8
import pygame
import pygameMenu
from pygameMenu.locals import *
from gamePackage.game import Game
from gamePackage.menu.options import OptionsMenu
from gamePackage.singleton import Singleton


class MainMenu(pygameMenu.menu.Menu, Singleton):

    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Screen size
        self.width = 832
        self.height = 832
        # Init the screen size
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Set title of the window
        pygame.display.set_caption('idk yet')
        self.font = pygameMenu.fonts.FONT_NEVIS
        super(MainMenu, self).__init__(self.screen, self.width, self.height, self.font,
                                       'idk yet', bgfun=lambda: self.screen.fill((0, 255, 100)))
        self.display_menu()

    def display_menu(self):
        self.add_option("New game", lambda: self.start_game())
        # TODO : Select a save file
        self.add_option("Load game", lambda: self.start_game())
        self.add_option("Options", lambda: OptionsMenu.get_instance(self.screen, (self.width, self.height)))
        self.add_option("Leave game", PYGAME_MENU_EXIT)
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def start_game(self):
        self.disable()
        Game.get_instance(self.screen)



