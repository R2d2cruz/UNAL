import json

import pygame

from .Entity import Entity
from .ResourceManager import resourceManager


class Wall(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = resourceManager.loadImage("ts1", (96, 64, width, height))


class Map:

    def __init__(self, mapName):
        self.name = mapName
        self.frames = {}
        self.jumpPoints = []
        self.objects = []
        self.cells = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.rows = 0
        self.cols = 0
        self.tileWidth = 32
        self.tileHeight = 32
        self.graph = None

        self.loadMap(resourceManager.getMap(mapName))
        self.createWalls(self.cells)

    def loadMap(self, fileName: str):
        self.cells = []
        tileSetName = None
        with open(fileName) as json_file:
            data = json.load(json_file)
            tileSetName = data.get("tileset")
            cells = data.get("cells")
            for row in cells:
                newRow = []
                for col in row:
                    newRow.append(col)
                self.cells.append(newRow)
        self.rows = len(self.cells)
        self.cols = len(self.cells[0])
        self.width = self.cols * self.tileWidth
        self.height = self.rows * self.tileHeight
        if tileSetName is not None:
            self.frames = self.loadTileset(resourceManager.getTileset(tileSetName))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @staticmethod
    def loadTileset(fileName: str):
        frames = {}
        with open(fileName) as json_file:
            data = json.load(json_file)
            image = resourceManager.loadImageByPath(resourceManager.fixPath(data.get("image")))
            for frame in data.get("tiles"):
                frames[frame["id"]] = image.subsurface(frame["box"])
        return frames

    def render(self, screen, camera):
        # TODO: optimizar la creacion del surface
        for row in range(self.rows):
            for col in range(self.cols):
                screen.blit(
                    self.frames.get(self.cells[row][col]),
                    camera.apply((
                        self.x + (self.tileWidth * col),
                        self.y + (self.tileHeight * row)
                    ))
                )
        for k in self.objects:
            k.render(screen, camera)

    def pointToCell(self, x, y):
        return str(int(x / self.tileWidth)) + ',' + str(int(y / self.tileHeight))

    def cellToPoint(self, cell):
        coord = cell.split(',')
        return [int(coord[0]) * self.tileWidth + self.tileWidth / 2,
                int(coord[1]) * self.tileHeight + self.tileHeight / 2]

    def createWalls(self, mapCells):
        for i in range(len(mapCells)):
            for j in range(len(mapCells[i])):
                if mapCells[i][j] == 1:
                    x = j * self.tileWidth
                    y = i * self.tileHeight
                    obj = Wall(x, y, self.tileWidth, self.tileHeight)
                    self.objects.append(obj)
