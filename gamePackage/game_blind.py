import pygame
from gamePackage.game import Game
from gamePackage.map.map import Map
from xml.etree import ElementTree as ET
import xml.dom.minidom


class GameBlind(Game):

    def __init__(self, screen, client):
        self.client = client
        super(Game, self).__init__(screen)

    def load_map(self, screen):
        map_name = self.search_map()
        map_path = "../map/%s" % map_name
        # Load the map
        self.map = Map(self, screen, map_path)
        self.map.draw_static_sprites()

    def search_map(self):
        map_order_file = "../map/map_order.xml"
        root = ET.parse(map_order_file).getroot()
        maps = root.findall('map')
        if done:
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

    def collide_with_walls(self, axis=None):
        """
        Check if the Character collide with any wall.
        Block the character in front of the wall if it's the case.
        Do it with x or y axis because if we do both at one time it does strange things. (ie the Player teleport)
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
