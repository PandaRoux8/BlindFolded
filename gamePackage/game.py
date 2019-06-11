# coding: utf-8
import sys
import pygame
from gamePackage.map.map import Map
from gamePackage.menu.main_menu import MainMenu


class Game(object):

    def __init__(self, from_death=False):
        # Initialize pygame
        pygame.init()
        # Set title of the window
        pygame.display.set_caption('Blindfolded')
        # TODO : get this from a file
        # Screen size
        self.width = 832
        self.height = 832
        # Init the screen size
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Frame rate (clock tick in the while true of the game)
        self.framerate = 15
        self.clock = pygame.time.Clock()
        # Save the main menu instance
        self.main_menu = None
        # Map loaded in the game
        self.map = None
        # Character of the player
        self.player = None

        # Set the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.static_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.kill_sprites = pygame.sprite.Group()
        self.finish_sprite = pygame.sprite.Group()
        self.teleporter_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()

        # Select a font for the game
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        # # When creating an instance start a new game
        # self.new_game()
        if not from_death:
            self.call_main_menu()
        self.__run_game()

    def call_main_menu(self):
        if not self.main_menu:
            self.main_menu = MainMenu(self.screen, (self.width, self.height))
        else:
            self.main_menu.enable()

    def new_game(self):
        # Load the map
        self.map = Map(self, "../map/map_1.tmx")
        self.map.draw_static_sprites()

    def __run_game(self):
        self.new_game()
        while True:
            self.clock.tick(self.framerate)
            self.player.check_exit_game()
            # Tick for the framerate
            # TODO : FIXME : Find out how this really works so it can be optimized (drawing updating etc.)
            self.map.draw()
            self.map.update()

    def collide_with_walls(self, axis=None):
        """
        Check if the Character collide with any wall.
        Block the character in front of the wall if it's the case.
        Do it with x or y axis because if we do both at one time it does strange things. (ie the Player teleport)
        """
        block_hit_list = pygame.sprite.spritecollide(self.player, self.block_sprites, dokill=False)
        for block in block_hit_list:
            if axis == 'x':
                if self.player.vx > 0:
                    self.player.rect.right = block.rect.left
                else:
                    self.player.rect.left = block.rect.right

            if axis == 'y':
                if self.player.vy > 0:
                    self.player.rect.bottom = block.rect.top
                else:
                    self.player.rect.top = block.rect.bottom

    def kill_on_collide(self):
        """
        Check if the player has fallen into a hole
        """
        block_hit_list = pygame.sprite.spritecollide(self.player, self.kill_sprites, dokill=False)
        if block_hit_list:
            self.game_over()

    def teleport_player(self):
        block_hit_list = pygame.sprite.spritecollide(self.player, self.teleporter_sprites, dokill=False)
        if len(block_hit_list) == 1 and self.player.has_moved:
            self.player.rect.x = block_hit_list[0].destination_x
            self.player.rect.y = block_hit_list[0].destination_y

    def finish_map(self):
        block_hit_list = pygame.sprite.spritecollide(self.player, self.finish_sprite, dokill=False)
        if block_hit_list:
            self.load_next_map()

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        :return:
        """
        # It's ugly but it works !
        text = self.font.render("GAME OVER", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to continue", 1, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)

        self.reload_game()

    def reload_game(self):
        """
        Reload a new game on the same map
        Delete the old instance of the game and start a new one
        """
        # FIXME : this could be optimized
        del self
        Game(from_death=True)

    def load_next_map(self):
        text = self.font.render("GOOD JOB ", 1, (255, 255, 255))
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
        text2 = font2.render("Press Space to go to next level", 1, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2))
        self.screen.blit(text2, (self.screen.get_width() / 2 - 95, self.screen.get_height() / 2 + 32))

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)
        self.reload_game()

    def exit_game(self):
        pygame.quit()
        sys.exit()
