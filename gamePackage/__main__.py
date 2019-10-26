import pygame
from gamePackage.menu import main_menu

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    # Set title of the window
    pygame.display.set_caption('Blindfolded')
    # Screen size
    width = 832
    height = 832
    # Init the screen size
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    main_menu = main_menu.MainMenu(screen, (width, height))
