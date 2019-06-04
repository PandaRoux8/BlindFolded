# coding: utf-8
import pygame
import pygameMenu


# Singleton object
class KeysMenu(pygameMenu.menu.Menu):
    __instance = None

    @staticmethod
    def get_instance(screen, resolution):
        print("Yo yo", KeysMenu.__instance)
        if not KeysMenu.__instance:
            KeysMenu(screen, resolution)
        return KeysMenu.__instance

    def __init__(self, screen, resolution):
        self.screen = screen
        width = resolution[0]
        height = resolution[1]
        super(KeysMenu, self).__init__(self.screen, width, height, pygameMenu.fonts.FONT_NEVIS,
                               'Keys', bgfun=lambda: self.screen.fill((0, 255, 100)))
        KeysMenu.__instance = self
        self.display_menu()

    def display_menu(self):
        self.add_option("Back", lambda: self.disable())
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)
