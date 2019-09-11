import sys
import pygame
from gamePackage.map.map import Map


class Game(object):

    def __init__(self, screen):
        print("YO GAME")
        # Map loaded in the game
        self.map = None
        # Character of the player
        self.blind = None

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
        self.blind_sprite = pygame.sprite.Group()

        self.load_map(screen)
        self.run_game()

    def load_map(self, screen):
        pass

    def run_game(self):
        while True:
            self.clock.tick(self.framerate)
            self.blind.check_exit_game()
            # Tick for the framerate
            # TODO : FIXME : Find out how this really works so it can be optimized (drawing updating etc.)
            self.map.draw()
            self.map.update()
            if self.server:
                self.server.blind = self.blind
                self.server.game = self
                self.server.listen()

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
        del self
        Game(screen, server=server, client=client)

    def load_next_map(self):
        self.map.display_end_level_message()
        self.search_map(done=True)

        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(30)
        self.reload_game()

    def exit_game(self):
        pygame.quit()
        sys.exit()
