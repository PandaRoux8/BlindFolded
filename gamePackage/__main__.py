import pygame
from gamePackage.menu import main_menu
from gamePackage import constants

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    # Set title of the window
    pygame.display.set_caption('Blindfolded')
    # Screen size
    width = constants.HEIGHT
    height = constants.WIDTH
    # Init the screen size
    screen = pygame.display.set_mode((width, height))
    main_menu = main_menu.MainMenu(screen)
