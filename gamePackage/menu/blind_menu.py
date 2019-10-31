import pygame
import pygameMenu
import errno
from time import sleep
from socket import error as socket_error
from gamePackage import constants
from gamePackage.menu import main_menu
from gamePackage.game_blind import GameBlind
from gamePackage.network.client import Client


class BlindMenu(pygameMenu.Menu):

    def __init__(self, screen):
        """
        :param screen: pygame.Screen object
        """
        self._screen = screen
        super(BlindMenu, self).__init__(self._screen, constants.WIDTH, constants.HEIGHT, constants.FONT,
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
        Connect to the Guide server
        """
        input_data = self.get_input_data()
        connected = False
        while not connected:
            try:
                client = Client(input_data.get('ip'))
                connected = True
            except socket_error as e:
                connected = False
                if e.errno != errno.ECONNREFUSED:
                    raise e
            sleep(0.5)
        screen = self._screen
        del self
        GameBlind(screen, client)
        BlindMenu.stop_client(client)

    @staticmethod
    def stop_client(client):
        """
        Close the connection with the server and close the client
        :param client: .Client object
        """
        client.release()
