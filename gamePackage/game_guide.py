from gamePackage.game import Game


class GameGuide(Game):

    def __init__(self, screen, server):
        self.server = server
        super(Game, self).__init__(screen)
