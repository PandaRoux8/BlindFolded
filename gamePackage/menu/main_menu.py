# coding: utf-8
import pygame
import pygameMenu
from pygameMenu.locals import *
# from gamePackage.game import Game
from gamePackage.menu.options import OptionsMenu


class MainMenu(pygameMenu.menu.Menu):

    def __init__(self, screen, resolution):
        # Init the screen size
        self.screen = screen
        self._width = resolution[0]
        self._height = resolution[1]
        self.font = pygameMenu.fonts.FONT_NEVIS
        super(MainMenu, self).__init__(self.screen, self._width, self._height, self.font,
                                       'Blindfolded', bgfun=lambda: self.screen.fill((0, 255, 100)))
        self.display_menu()

    def display_menu(self):
        self.add_option("New game", lambda: self.start_game())
        # TODO : Select a save file
        self.add_option("Load game", lambda: self.start_game())
        self.add_option("Leave game", PYGAME_MENU_EXIT)
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def start_game(self):
        self.disable()



