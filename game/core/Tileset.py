import json

import pygame

from . import resourceManager


class Tile:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walkable = True


class Tileset:
    def __init__(self, name: str):
        self.__clip = pygame.Rect(0, 0, 0, 0)
        self.__sheet = None
        self.__tiles = []
        self.name = name

    @property
    def tileWidth(self):
        return self.__clip.width

    @tileWidth.setter
    def tileWidth(self, width: int):
        self.__clip.width = width

    @property
    def tileHeight(self):
        return self.__clip.height

    @tileHeight.setter
    def tileHeight(self, height: int):
        self.__clip.height = height

    def getTileInfo(self, tileId: int):
        return self.__tiles[tileId]

    def getTileSurface(self, tileId: int):
        self.__clip.x = self.__tiles[tileId].x
        self.__clip.y = self.__tiles[tileId].y
        self.__sheet.set_clip(self.__clip)
        return self.__sheet.subsurface(self.__sheet.get_clip())

    @staticmethod
    def loadTileset(defName: str):
        fileDefName = resourceManager.getTileset(defName)
        tileset = Tileset(defName)
        with open(fileDefName) as jsonFile:
            data = json.load(jsonFile)
            tileset.__sheet = resourceManager.loadImageByPath(resourceManager.fixPath(data.get("image")))
            tileset.tileWidth = data.get("tileWidth")
            tileset.tileHeight = data.get("tileHeight")
            cols = int(tileset.__sheet.get_width() / tileset.tileWidth)
            rows = int(tileset.__sheet.get_height() / tileset.tileHeight)
            for row in range(rows):
                for col in range(cols):
                    tileset.__tiles.append(Tile(col * tileset.tileWidth, row * tileset.tileHeight))
            tiles = data.get("tiles")
            for tile in tiles:
                tileset.__tiles[tile.get("id")].walkable = tile.get("walkable")
        return tileset
