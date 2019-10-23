import pygame
from gamePackage.game_blind import GameBlind
import pygameMenu
from gamePackage.network.client import Client


class BlindMenu(pygameMenu.Menu):

    def __init__(self, screen, resolution):
        # Init the screen size
        self.screen = screen
        self._width = resolution[0]
        self._height = resolution[1]
        self.font = pygameMenu.font.FONT_NEVIS
        super(BlindMenu, self).__init__(self.screen, self._width, self._height, self.font, 'Connection Menu',
                                        bgfun=lambda: self.screen.fill((0, 255, 100)))
        # TODO : Show the lobby menu ... And start the game afterward
        self.display_menu()
        # Straight up start the game for testing purpose
        # GameBlind(self.screen, client)
        # client.release()

    def connect(self):
        input_data = self.get_input_data()
        client = Client(input_data.get('ip'))
        screen = self.screen
        self.disable()
        del self
        GameBlind(screen, client)
        client.release()

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
    #
    # def start_game(self):
    #     self.disable()
