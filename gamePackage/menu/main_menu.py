# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import pygame
import pygameMenu
from pygameMenu import locals
import constants
from menu.guide_menu import GuideMenu
from menu.blind_menu import BlindMenu


class MainMenu(pygameMenu.menu.Menu):

    def __init__(self, screen):
        """
        :param screen: pygame.Screen object
        """
        self._screen = screen
        super(MainMenu, self).__init__(self._screen, constants.WIDTH, constants.HEIGHT, constants.FONT,
                                       constants.WINDOW_TITLE, bgfun=lambda: self._screen.fill(constants.MENU_BG_COLOR),
                                       menu_color_title=constants.MENU_COLOR_TITLE, widget_alignment=locals.ALIGN_CENTER)
        self._set_widgets()
        self._display_menu()

    def _set_widgets(self):
        """
        Set the widgets for the menu
        """
        self.add_option("Play Guide", lambda: self._call_guide_menu())
        self.add_option("Play Blind", lambda: self._call_blind_menu())
        self.add_option("Leave game", pygameMenu.events.EXIT)

    def _display_menu(self):
        """
        Display the menu
        """
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def _call_guide_menu(self):
        """
        Call the Guide menu and deletes the current menu
        """
        screen = self._screen
        del self
        GuideMenu(screen)

    def _call_blind_menu(self):
        """
        Call the blind menu and deletes the current menu
        """
        screen = self._screen
        del self
        BlindMenu(screen)

    def _call_options(self):
        """
        Call the options menu and deletes the current menu
        """
        screen = self._screen
        del self
        OptionsMenu(screen)
