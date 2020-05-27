import json
import pygame
from core import Game, ResourceManager


class Map:
    map = [

    ]
    frames = {

    }

    jumpPoints = [

    ]

    objects = [

    ]

    characters = [

    ]

    def __init__(self, game: Game):
        self.game = game
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.rows = 0
        self.cols = 0
        self.tileWidth = 32
        self.tileHeight = 32

    def loadMap(self, fileName: str):
        map = []
        with open(fileName) as json_file:
            data = json.load(json_file)
            for row in data:
                newRow = []
                for col in row:
                    newRow.append(col)
                map.append(newRow)
        self.rows = len(map[0])
        self.cols = len(map)
        self.width = self.cols * self.tileWidth
        self.height = self.rows * self.tileHeight
        # self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        return map

    @staticmethod
    def loadTileset(fileName: str, res: ResourceManager):
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
                    camera.apply((self.x + (self.tileWidth * col),
                                  self.y + (self.tileHeight * row)))
                )
        for k in self.objects:
            k.render(screen, camera)
