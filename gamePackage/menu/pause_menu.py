# coding: utf-8
import sys
import pygame
import pygameMenu
from pygameMenu import locals
from gamePackage import constants


class PauseMenu(pygameMenu.Menu):

    def __init__(self, screen):
        """
        :param screen: pygame.Screen object
        """
        self._screen = screen
        super(PauseMenu, self).__init__(self._screen, constants.WIDTH, constants.HEIGHT, constants.FONT,
                                        constants.WINDOW_TITLE, bgfun=lambda: self._screen.fill(constants.MENU_BG_COLOR),
                                        menu_color_title=constants.MENU_COLOR_TITLE, widget_alignment=locals.ALIGN_CENTER)
        self._set_widgets()
        self._display_menu()

    def _set_widgets(self):
        """
        Set the widgets for the menu
        """
        self.add_option("Resume", lambda: self._resume())
        self.add_option("Leave game", pygameMenu.events.EXIT)

    def _display_menu(self):
        """
        Display the menu
        """
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def _resume(self):
        self.disable()
        del self
