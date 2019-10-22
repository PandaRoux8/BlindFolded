import pygame
from gamePackage.game_guide import GameGuide
import pygameMenu
from gamePackage.network.server import Server


class LobbyMenu(pygameMenu.Menu):

    # TODO ::
    def __init__(self, screen, resolution):
        # Init the screen size
        self.screen = screen
        self._width = resolution[0]
        self._height = resolution[1]
        self.font = pygameMenu.font.FONT_NEVIS
        super(LobbyMenu, self).__init__(self.screen, self._width, self._height, self.font, 'Connection Menu',
                                        bgfun=lambda: self.screen.fill((0, 255, 100)))
        # TODO : Show the lobby menu ... And start the game afterward
        self.display_menu()
        # server = LobbyMenu.start_server()
        # # TODO : Load menu instead
        # #  Straight up start the game for testing purpose
        # GameGuide(self.screen, server=server)
        # server.release()

    def connect(self):
        input_data = self.get_input_data()
        screen = self.screen
        server = LobbyMenu.start_server(input_data.get('ip'))
        self.disable()
        del self
        GameGuide(screen, server=server)
        server.release()

    @staticmethod
    def start_server(ip_address):
        server = Server(ip_address)
        # This method ends when a connection is made
        server.start_server()
        return server

    def display_menu(self):
        self.add_text_input("IP Address : ", textinput_id='ip', default='127.0.0.1', input_underline="_")
        self.add_option("Connect", lambda: self.connect())
        # TODO : Make this work
        self.add_option("Back", lambda: self._close())
        events = pygame.event.get()
        self.mainloop(events)

    # def display_menu(self):
    #     text = self.font.render("GOOD JOB ", 1, (255, 255, 255))
    #     font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
    #     text2 = font2.render("Press Space to go to next level", 1, (255, 255, 255))
    #     self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
    #     self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))
    #
    #     while not pygame.key.get_pressed()[pygame.K_SPACE]:
    #         pygame.event.pump()
    #         pygame.display.flip()
    #         self.clock.tick(30)

    # def start_game(self):
    #     self.disable()
