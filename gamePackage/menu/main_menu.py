import pygame
import pygameMenu
from gamePackage.menu.lobby import LobbyMenu
from gamePackage.menu.options import OptionsMenu
from gamePackage.menu.join_menu import JoinMenu


class MainMenu(pygameMenu.menu.Menu):

    def __init__(self, screen, resolution):
        # Init the screen size
        self.screen = screen
        self._width = resolution[0]
        self._height = resolution[1]
        self.font = pygameMenu.font.FONT_NEVIS
        super(MainMenu, self).__init__(self.screen, self._width, self._height, self.font,
                                       'Blindfolded', bgfun=lambda: self.screen.fill((0, 255, 100)))
        self.display_menu()

    def display_menu(self):
        # self.add_option("New game", lambda: self.start_game())
        self.add_option("Lobby", lambda: self._call_lobby())
        self.add_option("Join Game", lambda: self._call_join_menu())
        # TODO : Select a save file
        self.add_option("Leave game", pygameMenu.events.EXIT)
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def _call_lobby(self):
        self.disable()
        LobbyMenu(self.screen, (self._width, self._height))

    def _call_join_menu(self):
        self.disable()
        JoinMenu(self.screen, (self._width, self._height))

    def _call_options(self):
        self.disable()
        OptionsMenu(self.screen, (self._width, self._height))
