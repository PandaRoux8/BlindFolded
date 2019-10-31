# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import pygame
from game import AbstractGame
from map.map import Map
from menu.pause_menu import PauseMenu
from xml.etree import ElementTree as ET
import xml.dom.minidom


class GameBlind(AbstractGame):

    def __init__(self, screen, client, map_file=False):
        """
        :param screen: pygame.Screen object
        :param client:  .Client object
        :param map_file: String of the path for the map file
        """
        self.client = client
        self.map_path = map_file
        super(GameBlind, self).__init__(screen)

    def _load_map(self, screen):
        """
        Search for the map in the ./map/map_order.xml file and load it in the game.
        Then we send the map to the guide
        :param screen: .Screen object
        """
        if not self.map_path:
            map_name = self.search_map()
            self.map_path = "../map/%s" % map_name
        self.client.send_new_map(self.map_path, self.get_map_timer())
        # Load the map
        self.map = Map(self, screen, self.map_path, self.get_map_timer(), blind=True)
        self.map.draw_static_sprites()
        super(GameBlind, self)._load_map(screen)

    def _run_game(self):
        """
        Inherit _run_game to add the check for the timer of the map.
        """
        super(GameBlind, self)._run_game()
        if self.client:
            self.client.game = self
            self.client.get_pause_game()
        self.is_map_timer_done()

    def check_collision_with_walls(self, axis=None):
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

    def check_collision_with_kill_sprite(self):
        """
        Check if the blind has fallen into a hole
        """
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.kill_sprites, dokill=False)
        if block_hit_list:
            self.game_over()

    def check_collision_teleporter(self):
        """
        Teleport the blind to the other teleporter
        """
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.teleporter_sprites, dokill=False)
        if len(block_hit_list) == 1 and self.blind.has_moved:
            self.blind.rect.x = block_hit_list[0].destination_x
            self.blind.rect.y = block_hit_list[0].destination_y

    def check_end_level(self):
        """
        Check if the blind touched the finish sprite
        If it's the case we load the next level
        """
        block_hit_list = pygame.sprite.spritecollide(self.blind, self.finish_sprite, dokill=False)
        if block_hit_list:
            self.next_level()

    def reload_game(self, from_game_over=False):
        """
        Reload a new game
        Delete the old instance of the game and start a new one
        """
        # Wait for the guide to be ready
        self.client.check_server_ready()
        screen = self.map.screen
        client = self.client
        map_path = False
        if from_game_over:
            map_path = self.map_path
        del self
        GameBlind(screen, client, map_path)

    def game_over(self):
        """
        Display game over on screen
        Restart a new game
        """
        self.client.send_display_game_over()
        super(GameBlind, self).game_over()

    def next_level(self):
        """
        Displays next_level message and send it to the guide as well
        Then load the next level map
        """
        self.client.send_display_next_level()
        self.search_map()
        super(GameBlind, self).next_level()

    def pause_game(self):
        PauseMenu(self.screen)
        self.client.check_server_ready()

    def exit_game(self):
        """
        Close client connection and exit the game
        """
        self.client.release()
        super(GameBlind, self).exit_game()

    def is_map_timer_done(self):
        """
        Check if the timer is done
        """
        if self.map.timer_done:
            self.game_over()

    @staticmethod
    def get_map_timer():
        """
        Get the time of the current map
        """
        map_order_file = "../map/map_order.xml"
        root = ET.parse(map_order_file).getroot()
        maps = root.findall('map')
        for map in maps:
            if eval(map.get('current')):
                return map.get('timer')

    @staticmethod
    def search_map():
        """
        Search for the next map in the ./map/map_order.xml file
        """
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
