import json
import pygame
import core.ResourceManager as res
from core import ResourceManager


class Map:
    frames = {

    }

    jumpPoints = [

    ]

    objects = [

    ]

    def __init__(self):
        self.map = []
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
            image = res.loadImageByPath(res.fixPath(data.get("image")))
            for frame in data.get("tiles"):
                frames[frame["id"]] = image.subsurface(frame["box"])
        return frames

    def render(self, screen, camera):
        # TODO: optimizar la creacion del surface
        for row in range(self.rows):
            for col in range(self.cols):
                screen.blit(
                    self.frames.get(self.map[row][col]),
                    camera.apply(
                        (self.x + (self.tileWidth * col),
                         self.y + (self.tileHeight * row))
                    )
                )
        for k in self.objects:
            k.render(screen, camera)

    def getGraph(self):
        graph = {}
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                if self.map[row][col] == 0:
                    graph[str(col) + ',' + str(row)] = self.getNeighbors(col, row)

        def countNeighbors(nodeKey):
            return -len(graph[nodeKey])

        for nodeKey in graph:
            graph[nodeKey] = sorted(graph[nodeKey], key=countNeighbors)
        return graph

    def getNeighbors(self, col, row):
        nodes = []
        for y in range(row - 1, row + 2):
            if 0 <= y < self.rows:
                for x in range(col - 1, col + 2):
                    if 0 <= x < self.cols:
                        if self.map[y][x] == 0 and self.map[y][col] == 0 and self.map[row][x] == 0:
                            nodes.append(str(x) + ',' + str(y))
        return nodes

    def pointToCell(self, x, y):
        return str(int(x / self.tileWidth)) + ',' + str(int(y / self.tileHeight))

    def cellToPoint(self, cell):
        coord = cell.split(',')
        return [int(coord[0]) * self.tileWidth + self.tileWidth / 2, int(coord[1]) * self.tileHeight + self.tileHeight / 2]
