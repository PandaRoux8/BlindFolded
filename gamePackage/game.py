import sys
import pygame
from gamePackage.network.client import Client
from gamePackage.map.map import Map


class Game(object):

    def __init__(self, screen, map=False, from_death=False, server=False, client=False):
        # Map loaded in the game
        self.map = None
        # Character of the player
        self.player = None
        self.server = server
        self.client = client

        # TODO : Get these from __main__ ? Or from a file ?
        # Game clock
        self.clock = pygame.time.Clock()
        self.framerate = 15

        # Set the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.static_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.kill_sprites = pygame.sprite.Group()
        self.finish_sprite = pygame.sprite.Group()
        self.teleporter_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()

        if map:
            self.load_map(screen, map)
        self.__run_game()

    def load_map(self, screen, map):
        # Load the map
        self.map = Map(self, screen, "../map/map_1.tmx")
        self.map.draw_static_sprites()

    def __run_game(self):
        while True:
            if self.server:
                self.server.player = self.player
                self.server.game = self
                self.server.listen()
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
        self.map.display_game_over()

        # TODO : More MVC ? Place it on the controller
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
        if self.client:
            self.client.send_new_map()
        screen = self.map.screen
        server = self.server
        client = self.client
        # TODO : How do we do this ? We need to pass screen here
        del self
        Game(screen, map='truc', from_death=True, server=server, client=client)

    def load_next_map(self):
        self.map.display_end_level_message()

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)
        self.reload_game()

    def exit_game(self):
        pygame.quit()
        sys.exit()
