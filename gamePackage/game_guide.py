from gamePackage.game import AbstractGame
from gamePackage.map.map import Map


class GameGuide(AbstractGame):

    def __init__(self, screen, server):
        self.server = server
        super(GameGuide, self).__init__(screen)

    def _load_map(self, screen):
        """
        Load the map
        :param screen: pygame.Screen object
        """
        # Wait for map to be loaded on blind and sent here
        while not self.server.map:
            self.server.listen()
        map_path = self.server.map
        # Load the map
        self.map = Map(self, screen, map_path, self.server.map_timer)
        self.map.draw_static_sprites()
        super(GameGuide, self)._load_map(screen)

    def _run_game(self):
        """
        Inherit run game to add the listening for the server on each iteration
        """
        super(GameGuide, self)._run_game()
        if self.server:
            self.server.blind = self.blind
            self.server.game = self
            self.server.listen()

    def reload_game(self, from_game_over=False):
        """
        Reload a new game
        Delete the old instance of the game and start a new one
        from_game_over : from_game_over is True we load the current map, otherwise we load the next map
        """
        # Wait for the blind to be ready
        self.server.check_client_ready()
        screen = self.map.screen
        self.server.map = False  # Reset the map so we always get the one from the blind
        server = self.server
        del self
        GameGuide(screen, server)

    def exit_game(self):
        self.server.release()
        super(GameGuide, self).exit_game()

