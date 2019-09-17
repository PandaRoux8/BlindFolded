from gamePackage.game import Game
from gamePackage.map.map import Map


class GameGuide(Game):

    def __init__(self, screen, server):
        self.server = server
        super(GameGuide, self).__init__(screen)

    def load_map(self, screen):
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

    def reload_game(self):
        screen = self.map.screen
        server = self.server
        del self
        GameGuide(screen, server)
