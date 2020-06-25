import json

import pygame

from .Entity import Entity
from .ResourceManager import resourceManager
from .Tileset import Tileset


class Wall(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = resourceManager.loadImage("ts1", (96, 64, width, height))
        self.type = "wall"


class TiledMap:

    def __init__(self, mapName):
        self.name = mapName
        self.tileset = None
        self.cells = []
        self.objects = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.rows = 0
        self.cols = 0
        self.graph = None
        self.loadMap(resourceManager.getMap(mapName))

    def loadMap(self, fileName: str):
        self.cells = []
        with open(fileName) as json_file:
            data = json.load(json_file)
            tileSetName = data.get("tileset")
            if tileSetName is not None:
                self.tileset = Tileset.loadTileset(tileSetName)
            else:
                print('❌ Error cargando mapa', fileName, ': tileset sin especificar')
            self.rows = data.get("rows")
            self.cols = data.get("cols")
            cells = data.get("cells")
            for row in cells:
                newRow = []
                for col in row:
                    newRow.append(col)
                if self.cols != len(newRow):
                    print('❌ Error cargando mapa', fileName, ': número de columnas no coincide ', self.cols, '<>',
                          len(newRow))
                self.cells.append(newRow)
            objs = data.get('objects')
            if objs is not None:
                for obj in objs:
                    pos = obj.get('pos')
                    entity = Entity()
                    entity.tangible = obj.get('walkable')
                    entity.image = self.tileset.getTileSurface(obj.get("tile"))
                    entity.setPos(pos[0] * self.tileset.tileWidth, pos[1] * self.tileset.tileHeight)
                    self.objects.append(entity)
        if self.rows != len(self.cells):
            print('❌ Error cargando mapa', fileName, ': número de filas no coincide', self.rows, '<>', len(self.cells))
        self.width = self.cols * self.tileset.tileWidth
        self.height = self.rows * self.tileset.tileHeight

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface, camera):
        for row in range(self.rows):
            for col in range(self.cols):
                surface.blit(
                    self.tileset.getTileSurface(self.cells[row][col]),
                    camera.apply((
                        self.x + (self.tileset.tileWidth * col),
                        self.y + (self.tileset.tileHeight * row)
                    ))
                )
        # for obj in self.objects:
        #     obj.render(surface, camera)

    def pointToCell(self, x, y):
        return str(int(x / self.tileset.tileWidth)) + ',' + str(int(y / self.tileset.tileHeight))

    def cellToPoint(self, cell):
        coord = cell.split(',')
        return [int(coord[0]) * self.tileset.tileWidth + self.tileset.tileWidth / 2,
                int(coord[1]) * self.tileset.tileHeight + self.tileset.tileHeight / 2]

    def getWalls(self):
        walls = []
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                tile = self.tileset.getTileInfo(self.cells[i][j])
                if not tile.walkable:
                    x = j * self.tileset.tileWidth
                    y = i * self.tileset.tileHeight
                    obj = Wall(x, y, self.tileset.tileWidth, self.tileset.tileHeight)
                    walls.append(obj)
        return walls
