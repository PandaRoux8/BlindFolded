import pygame
from gamePackage.game import Game
# import pygameMenu
# from pygameMenu.locals import *
from gamePackage.network.server import Server
import threading


class LobbyMenu(object):

    # TODO ::
    def __init__(self, screen, resolution):
        # Init the screen size
        self.screen = screen
        self._width = resolution[0]
        self._height = resolution[1]
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        super(LobbyMenu, self).__init__()
        server = LobbyMenu.start_server()
        # Straight up start the game for testing purpose
        Game(self.screen, map='truc', guide=True, server=server)
        # TODO : Show the lobby menu ... And start the game afterward
        # self.display_menu()

    @staticmethod
    def start_server():
        server = Server()
        # Daemon -> We don't have to worry about stopping the thread it stops when program exits
        thread = threading.Thread(target=server.start_server(), daemon=True)
        thread.start()
        return server

    def display_menu(self):
        text = self.font.render("GOOD JOB ", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to go to next level", 1, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)

    def start_game(self):
        self.disable()
