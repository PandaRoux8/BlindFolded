# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import pygame
import pygameMenu
import constants
from menu import main_menu
from game_guide import GameGuide
from network.server import Server


class GuideMenu(pygameMenu.Menu):

    def __init__(self, screen):
        """
        :param screen: pygame.Screen object
        """
        self._screen = screen
        super(GuideMenu, self).__init__(self._screen, constants.WIDTH, constants.HEIGHT, constants.FONT,
                                        constants.WINDOW_TITLE, bgfun=lambda: self._screen.fill(constants.MENU_BG_COLOR),
                                        menu_color_title=constants.MENU_COLOR_TITLE)
        self._set_widgets()
        self._display_menu()

    def _set_widgets(self):
        """
        Set the widgets for the menu
        """
        self.add_text_input("IP Address : ", textinput_id='ip', default='127.0.0.1', input_underline="_", maxchar=15)
        self.add_option("Connect", lambda: self._connect())
        self.add_option("Back", lambda: self._back_to_main_menu())

    def _display_menu(self):
        """
        Display the menu
        """
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def _back_to_main_menu(self):
        """
        Deletes the current menu, and init the .MainMenu
        """
        screen = self._screen
        del self
        main_menu.MainMenu(screen)

    def _connect(self):
        """
        Connect to the blind player
        """
        input_data = self.get_input_data()
        screen = self._screen
        server = GuideMenu.start_server(input_data.get('ip'))
        del self
        GameGuide(screen, server=server)
        GuideMenu.stop_server(server)

    @staticmethod
    def start_server(ip_address):
        """
        Start the server and wait for a connection
        :param ip_address: ip address of the client
        :return .Server object
        """
        server = Server(ip_address)
        # This method ends when a connection is made
        server.start_server()
        return server

    @staticmethod
    def stop_server(server):
        """
        Close connection and stop the server
        :param server: .Server object
        """
        server.release()
