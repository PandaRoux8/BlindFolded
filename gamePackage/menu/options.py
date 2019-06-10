# coding: utf-8
import pygame
import pygameMenu
from gamePackage.menu.keys_menu import KeysMenu


# Singleton object
class OptionsMenu(pygameMenu.menu.Menu):
    def __init__(self, screen, resolution):
        self.screen = screen
        self.width = resolution[0]
        self.height = resolution[1]
        # set a default display
        # self.display = None
        super(OptionsMenu, self).__init__(self.screen, self.width, self.height, pygameMenu.fonts.FONT_NEVIS,
                               'Options', bgfun=lambda: self.screen.fill((0, 255, 100)))
        OptionsMenu.__instance = self
        self.display_menu()

    # def change_display(self, display):
    #     self.display = display

    # def change_resolution(self, resolution):
    #     print("YOYOYOY")
    #     self.width = resolution[0]
    #     self.height = resolution[1]

    def display_menu(self):
        self.add_selector('Display', [('Windowed', 'windowed'), ('Fullscreen', 'fullscreen')], None, None, write_on_console=True)
        # self.add_selector('Resolution',
        #                   [
        #                     ('2560x1080', (2560, 1080)),
        #                     ('1920x1080', (1920, 1080)),
        #                     ('1680x1050', (1600, 900)),
        #                     ('1600x900', (1600, 900)),
        #                     ('1440x900', (1440, 900)),
        #                     ('1366x768', (1366, 768)),
        #                     ('1280x1024', (1280, 1024)),
        #                   ],
        #                   lambda: self.change_resolution(),  # FIXME -> This does not work
        #                   None,
        #                   write_on_console=True
        # )
        self.add_option("Keys", lambda: KeysMenu.get_instance(self.screen, (self.width, self.height)))
        self.add_option("Back", lambda: self.disable())
        self.enable()
        events = pygame.event.get()
        self.mainloop(events)

    def disable(self):
        """
        Override the disable method so when it closes we save the configuration in a file.
        """
        super(OptionsMenu, self).disable()
        file_path = "./saves/config_options.save"
        self.write_save_file(file_path)

    def write_save_file(self, file_path):
        """
        Rewrite the whole file since it's a small file.
        FIXME : Optimize this to write only if there's modification
        """
        with open(file_path, "w+") as file:
            file.write("resolution:(%s,%s)\n" % (str(self.width), str(self.height)))
            file.write("display:%s\n" % str(self.display))
