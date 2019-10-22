from gamePackage.game import AbstractGame
from gamePackage.map.map import Map


class GameGuide(AbstractGame):

    def __init__(self, screen, server):
        self.server = server
        super(GameGuide, self).__init__(screen)

    def load_map(self, screen):
        """
        Load the map
        :param screen:
        :return:
        """
        # Wait for map to be loaded
        while not self.server.map:
            self.server.listen()
        map_path = self.server.map
        # Load the map
        self.map = Map(self, screen, map_path)
        self.map.draw_static_sprites()
        super(GameGuide, self).load_map(screen)

    def run_game(self):
        super(GameGuide, self).run_game()
        if self.server:
            self.server.blind = self.blind
            self.server.game = self
            self.server.listen()

    def reload_game(self, from_game_over=False):
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

