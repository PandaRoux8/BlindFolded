# coding: utf-8
import pygame


class NPC(pygame.sprite.Sprite):

    def __init__(self, game, tile, x, y):
        super(NPC, self).__init__()
        self.__game = game
        self._message = "Suh mah dude"
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def talk(self):
        # It's ugly but it works !
        text = self.__game.font.render(self._message, 1, (255, 255, 255))
        screen = self.__game.screen
        dialog_box_pos = (screen.get_width() / 2, screen.get_height()-64)
        dialog_box_size = (200, 64)

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(dialog_box_pos, dialog_box_size))

        self.__game.screen.blit(text, (screen.get_width() / 2, screen.get_height()-64))
        while not pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
            pygame.display.flip()
            self.__game.clock.tick(60)

    def give_object(self):
        pass
