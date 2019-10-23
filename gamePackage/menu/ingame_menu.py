# coding: utf-8
import pygame
import pygameMenu


# Singleton object
class InGameMenu(pygameMenu.Menu):
    __instance = None

    @staticmethod
    def get_instance(screen, resolution):
        if not InGameMenu.__instance:
            InGameMenu(screen, resolution)
        return InGameMenu.__instance

    def __init__(self, screen, resolution):
        self.screen = screen
        self.width = resolution[0]
        self.height = resolution[1]
        # set a default display
        self.display = None
        super(InGameMenu, self).__init__(self.screen, self.width, self.height, pygameMenu.font.FONT_NEVIS,
                                         'Options', bgfun=lambda: self.screen.fill((0, 255, 100)))
        InGameMenu.__instance = self
        self.add_option("Back to game", lambda: self.disable())
        self.add_option("Leave game", lambda: pygame.quit())  # FIXME : This works but it's an error

    def display_menu(self):
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)
