# coding: utf-8
import pygame
import pygameMenu
from pygameMenu.locals import *
from gamePackage.game.game import Game
from gamePackage.menu.options import OptionsMenu


class MainMenu(pygameMenu.menu.Menu):
    __instance = None

    @staticmethod
    def get_instance():
        if not MainMenu.__instance:
            MainMenu()
        return MainMenu.__instance

    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Screen size
        self.width = 1600
        self.height = 900
        # Init the screen size
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Set title of the window
        pygame.display.set_caption('idk yet')
        self.font = pygameMenu.fonts.FONT_NEVIS
        super(MainMenu, self).__init__(self.screen, self.width, self.height, self.font,
                                       'idk yet', bgfun=lambda: self.screen.fill((0, 255, 100)))
        self.display_menu()

    def display_menu(self):
        self.add_option("New game", lambda: Game(self.screen))
        # TODO : Select a save file
        self.add_option("Load game", lambda: Game(self.screen))
        self.add_option("Options", lambda: OptionsMenu.get_instance(self.screen, (self.width, self.height)))
        self.add_option("Leave game", PYGAME_MENU_EXIT)
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

