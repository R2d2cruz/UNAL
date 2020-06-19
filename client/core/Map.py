import json

import pygame

from .ResourceManager import resourceManager


class Map:
    frames = {

    }

    jumpPoints = [

    ]

    objects = [

    ]

    def __init__(self):
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

    def loadMap(self, fileName: str):
        map = []
        with open(fileName) as json_file:
            data = json.load(json_file)
            for row in data:
                newRow = []
                for col in row:
                    newRow.append(col)
                map.append(newRow)
        self.rows = len(map)
        self.cols = len(map[0])
        self.width = self.cols * self.tileWidth
        self.height = self.rows * self.tileHeight
        # self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        return map

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
                    camera.apply(
                        (self.x + (self.tileWidth * col),
                         self.y + (self.tileHeight * row))
                    )
                )
        for k in self.objects:
            k.render(screen, camera)

    def pointToCell(self, x, y):
        return str(int(x / self.tileWidth)) + ',' + str(int(y / self.tileHeight))

    def cellToPoint(self, cell):
        coord = cell.split(',')
        return [int(coord[0]) * self.tileWidth + self.tileWidth / 2, int(coord[1]) * self.tileHeight + self.tileHeight / 2]
