import pygame
import pygameMenu
from gamePackage import constants
from gamePackage.menu.guide_menu import GuideMenu
from gamePackage.menu.options import OptionsMenu
from gamePackage.menu.blind_menu import BlindMenu


class MainMenu(pygameMenu.menu.Menu):

    def __init__(self, screen):
        # Init the screen size
        self.screen = screen
        super(MainMenu, self).__init__(self.screen, constants.WIDTH, constants.HEIGHT, constants.FONT,
                                       constants.WINDOW_TITLE, bgfun=lambda: self.screen.fill(constants.MENU_COLOR))
        self.display_menu()

    def display_menu(self):
        self.add_option("Play Guide", lambda: self._call_guide_menu())
        self.add_option("Play Blind", lambda: self._call_blind_menu())
        self.add_option("Leave game", pygameMenu.events.EXIT)
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def _call_guide_menu(self):
        self.disable()
        GuideMenu(self.screen)

    def _call_blind_menu(self):
        self.disable()
        BlindMenu(self.screen)

    def _call_options(self):
        self.disable()
        OptionsMenu(self.screen)
