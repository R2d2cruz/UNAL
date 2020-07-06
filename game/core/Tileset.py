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
        self.__tileStart = 0
        self.name = name

    @property
    def tileStart(self):
        return self.__tileStart

    @tileStart.setter
    def tileStart(self, tileStart: int):
        self.__tileStart = tileStart

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
        if tileId < self.__tileStart:
            self.__sheet.set_clip()
            return self.__sheet.subsurface(self.__sheet.get_clip())
        self.__clip.x = self.__tiles[tileId - self.__tileStart].x
        self.__clip.y = self.__tiles[tileId - self.__tileStart].y
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
            tileset.tileStart = data.get("tileStart")
            cols = int(tileset.__sheet.get_width() / tileset.tileWidth)
            rows = int(tileset.__sheet.get_height() / tileset.tileHeight)
            for row in range(rows):
                for col in range(cols):
                    tileset.__tiles.append(Tile(col * tileset.tileWidth, row * tileset.tileHeight))
            tiles = data.get("tiles")
            for tile in tiles:
                tileId = tile.get("id") # - tileset.tileStart
                if 0 <= tileId < len(tileset.__tiles):
                    tileset.__tiles[tileId].walkable = tile.get("walkable")
        return tileset
