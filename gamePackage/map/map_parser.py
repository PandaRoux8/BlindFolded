# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

# coding: utf-8
import pygame
import constants
from xml.etree import ElementTree as ET


class MapParser(object):
    def __init__(self, file, blind=False):
        """
        :param file: path for the XML file containing the map
        """
        self._file = ET.parse(file)
        self._root = ET.parse(file).getroot()
        self.array_map = self.get_map()
        self.tile = self.get_tile(blind)

    def get_width(self):
        """
        Get the width of the map from the XML file
        """
        res = None
        if self._root.tag == 'map':
            res = self._root.attrib.get('width')
            res = not res or int(res)
        return res

    def get_height(self):
        """
        Get height of the map from the XML file
        """
        res = None
        if self._root.tag == 'map':
            res = self._root.attrib.get('height')
            res = not res or int(res)
        return res

    def get_tile_width(self):
        """
        Get width of tiles from the XML file
        """
        res = None
        if self._root.tag == 'map':
            res = self._root.attrib.get('tilewidth')
            res = not res or int(res)
        return res

    def get_tile_height(self):
        """
        Get height of tiles from the XML file
        """
        res = None
        if self._root.tag == 'map':
            res = self._root.attrib.get('tileheight')
            res = not res or int(res)
        return res

    def get_map(self):
        """
        Parse the given XML file and make a 2 dimension array with the tiles id
        """
        # Don't take layer into account for now
        data = self._root.find('layer').find('data')
        data_clean = data.text.replace('\n', '')

        # Only support left-down for now
        map = []
        rows = []
        width = self.get_width()
        for i, value in enumerate(data_clean.split(',')):
            rows.append(int(value))
            # Every time you reach the width of the map, make a new col
            if (i+1) % width == 0:
                map.append(rows)
                rows = []
        return map

    def get_tile(self, blind):
        """
        Get the tile from the map.tsx file
        :return: List of tiles (pygame.Surface)
        """
        if not blind:
            tile_file = self._root.find('tileset').attrib.get('source')
            tile_path = constants.DIR_MAP + tile_file
        else:
            tile_file = self._root.find('tileset').attrib.get('source')
            tile_file = tile_file.replace("default_tileset.tsx", "blind_tileset.tsx")
            tile_path = constants.DIR_MAP + tile_file
        return self.split_tile(tile_path)

    def split_tile(self, tile_file):
        """
        We have an image and we need to cut it in piece of 32 pixel by 32 pixel.
        These cuts are the tiles of the game
        :param tile_file: path to the tile.tsx file
        :return: List of tiles (pygame.Surface)
        """
        tile = ET.parse(tile_file)
        image = tile.getroot().find('image')
        source_img = image.attrib.get('source')
        img_path = constants.DIR_TILESET + source_img
        image = pygame.image.load(img_path).convert()
        image_width, image_height = image.get_size()
        tiles = []

        tile_width = self.get_tile_width()
        tile_height = self.get_tile_height()
        for x in range(int(image_width/tile_width)):
            for y in range(int(image_height/tile_height)):
                rect = (y*tile_width, x*tile_height,
                        tile_width, tile_height)
                tiles.append(image.subsurface(rect))
        return tiles
