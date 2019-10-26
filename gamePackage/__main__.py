import pygame
from gamePackage import constants
from gamePackage.menu import main_menu

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    # Set title of the window
    pygame.display.set_caption(constants.WINDOW_TITLE)
    # Screen size
    width = constants.HEIGHT
    height = constants.WIDTH
    # Init the screen size
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    main_menu = main_menu.MainMenu(screen)
