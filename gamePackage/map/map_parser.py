# coding: utf-8
from xml.etree import ElementTree as ET
import pygame
import sys


class MapParser(object):
    def __init__(self, file):
        print(file)
        print(sys.path)
        self.__file = ET.parse(file)
        self.__root = ET.parse(file).getroot()
        self._width = self._get_width()
        self._height = self._get_height()
        self._tileHeight = self._get_tile_height()
        self._tileWidth = self._get_tile_width()
        self.map = self.get_map()
        self.tile = self.get_tile()

    def _get_width(self):
        res = None
        if self.__root.tag == 'map':
            res = self.__root.attrib.get('width')
            res = not res or int(res)
        return res

    def _get_height(self):
        res = None
        if self.__root.tag == 'map':
            res = self.__root.attrib.get('height')
            res = not res or int(res)
        return res

    def _get_tile_width(self):
        res = None
        if self.__root.tag == 'map':
            res = self.__root.attrib.get('tilewidth')
            res = not res or int(res)
        return res

    def _get_tile_height(self):
        res = None
        if self.__root.tag == 'map':
            res = self.__root.attrib.get('tileheight')
            res = not res or int(res)
        return res

    def get_map(self):
        # Don't take layer into account for now
        data = self.__root.find('layer').find('data')
        data_clean = data.text.replace('\n', '')

        # Only support left-down for now
        map = []
        rows = []
        for i, value in enumerate(data_clean.split(',')):
            rows.append(int(value))
            # Every x we make a new col
            if (i+1) % self._width == 0:
                map.append(rows)
                rows = []
        return map

    def get_tile(self):
        # tile_dir = "./map/"
        # tile_file = self.__root.find('tileset').attrib.get('source')
        # tile_path = tile_dir + tile_file
        tile_path = "/opt/BlindFolded/map/tileset/default_tileset.tsx"  # TODO : FIX HARDCODE
        return self.split_tile(tile_path)

    def split_tile(self, tile_file):
        tile = ET.parse(tile_file)
        image = tile.getroot().find('image')
        source_img = image.attrib.get('source')
        img_path = "/opt/BlindFolded/map/tileset/" + source_img  # TODO : FIX HARDCODE
        image = pygame.image.load(img_path).convert()
        image_width, image_height = image.get_size()
        tiles = []

        for x in range(int(image_width/self._tileWidth)):
            for y in range(int(image_height/self._tileHeight)):
                rect = (y*self._tileWidth, x*self._tileHeight,
                        self._tileWidth, self._tileHeight)
                tiles.append(image.subsurface(rect))
        return tiles

    def display_tile(self):
        """
        Testing purpose
        """
        pygame.display.get_surface()
        for i, tile in enumerate(self.tile):
            pygame.display.get_surface().blit(tile, (i*32, 0))
