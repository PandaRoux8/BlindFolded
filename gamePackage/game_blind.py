import pygame
from gamePackage.game import AbstractGame
from gamePackage.map.map import Map
from xml.etree import ElementTree as ET
import xml.dom.minidom


class GameBlind(AbstractGame):

    def __init__(self, screen, client, map_file=False):
        self.client = client
        self.map_path = map_file
        super(GameBlind, self).__init__(screen)

    def load_map(self, screen):
        if not self.map_path:
            map_name = self.search_map()
            self.map_path = "../map/%s" % map_name
        self.client.send_new_map(self.map_path, self.get_map_timer())
        # Load the map
        self.map = Map(self, screen, self.map_path, self.get_map_timer())
        self.map.draw_static_sprites()
        super(GameBlind, self).load_map(screen)

    def run_game(self):
        super(GameBlind, self).run_game()
        self.is_map_timer_done()

    @staticmethod
    def search_map():
        map_order_file = "../map/map_order.xml"
        root = ET.parse(map_order_file).getroot()
        maps = root.findall('map')
        getnext = False
        for map in maps:
            if getnext:
                map.set('current', 'True')
                break
            if eval(map.get('current')):
                map.set('current', 'False')
                getnext = True

        with open(map_order_file, 'w') as f:
            ugly_xml = xml.dom.minidom.parseString(ET.tostring(root))
            xml_pretty_str = ugly_xml.toprettyxml()
            f.write(xml_pretty_str)

        for map in maps:
            if eval(map.get('current')):
                return map.text

        # TODO : Display end of game, for now we just return to map 1
        map1 = root.find('map')
        map1.set('current', 'True')
        with open(map_order_file, 'w') as f:
            ugly_xml = xml.dom.minidom.parseString(ET.tostring(root))
            xml_pretty_str = ugly_xml.toprettyxml()
            f.write(xml_pretty_str)

        return map1.text

    @staticmethod
    def get_map_timer():
        map_order_file = "../map/map_order.xml"
        root = ET.parse(map_order_file).getroot()
        maps = root.findall('map')
        for map in maps:
            if eval(map.get('current')):
                return map.get('timer')

    def collide_with_walls(self, axis=None):
        """
        Check if the Character collide with any wall.
        Block the character in front of the wall if it's the case.
        Do it with x or y axis because if we do both at one time it does strange things. (ie the blind teleport)
        """
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.block_sprites, dokill=False)
        for block in block_hit_list:
            if axis == 'x':
                if self.blind.vx > 0:
                    self.blind.rect.right = block.rect.left
                else:
                    self.blind.rect.left = block.rect.right

            if axis == 'y':
                if self.blind.vy > 0:
                    self.blind.rect.bottom = block.rect.top
                else:
                    self.blind.rect.top = block.rect.bottom

    def kill_on_collide(self):
        """
        Check if the blind has fallen into a hole
        """
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.kill_sprites, dokill=False)
        if block_hit_list:
            self.game_over()

    def teleport_blind(self):
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.teleporter_sprites, dokill=False)
        if len(block_hit_list) == 1 and self.blind.has_moved:
            self.blind.rect.x = block_hit_list[0].destination_x
            self.blind.rect.y = block_hit_list[0].destination_y

    def finish_map(self):
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.finish_sprite, dokill=False)
        if block_hit_list:
            self.load_next_map()

    def reload_game(self, from_game_over=False):
        """
        Reload a new game
        Delete the old instance of the game and start a new one
        """
        # Wait for the guide to be ready
        self.client.check_server_ready()
        # self.client.send_new_map()
        screen = self.map.screen
        client = self.client
        map_path = False
        if from_game_over:
            map_path = self.map_path
        # client.send_reload_game()
        del self
        GameBlind(screen, client, map_path)

    def is_map_timer_done(self):
        if self.map.timer_done:
            self.game_over()

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        :return:
        """
        self.client.send_display_game_over()
        super(GameBlind, self).game_over()

    def load_next_map(self):
        self.client.send_display_next_level()
        self.search_map()
        super(GameBlind, self).load_next_map()

    def exit_game(self):
        self.client.release()
        super(GameBlind, self).exit_game()
