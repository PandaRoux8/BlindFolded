import pygame
from gamePackage.menu import main_menu

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    # Set title of the window
    pygame.display.set_caption('Blindfolded')
    # TODO : get this from a file
    # Screen size
    # TODO : We'll need to read a save file to know the use conf
    width = 832
    height = 832
    # Init the screen size
    screen = pygame.display.set_mode((width, height))
    # Frame rate (clock tick in the while true of the game)
    framerate = 15
    clock = pygame.time.Clock()
    main_menu = main_menu.MainMenu(screen, (width, height))
