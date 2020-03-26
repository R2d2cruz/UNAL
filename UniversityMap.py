import pygame

from Player import Player
from Backgroung import Background
from Wanders import Wander
from Objects import *

class UniversityMap(Background):
    rect = 32
    #
    # 0 = grass
    # 1 = bricks
    # 2 = grass_brick left
    # 3 = grass_brick right
    # 4 = grass_brick supirior left
    # 5 = grass_brick inferior left
    # 6 = grass_brick up
    # 7 = grass_brick down
    # 20x9
    #
    #

    def __init__(self):
        self.player = Player((640, 360))
        self.x = self.player.get_x()
        self.y = self.player.get_y()
        image = pygame.image.load("RPG Nature Tileset.png")
        self.frames = {
            0: image.subsurface((0, 64, 32, 32)),
            1: image.subsurface((64, 64, 32, 32)),
            2: image.subsurface((0, 128, 32, 32)),
            3: image.subsurface((64, 128, 32, 32)),
            4: image.subsurface((0, 96, 32, 32)),
            5: image.subsurface((0, 160, 32, 32)),
            6: image.subsurface((32, 96, 32, 32)),
            7: image.subsurface((32, 160, 32, 32))
        }
        self.characters = [
            Wander((20, 0), [[0, 0], [200, 0]], [[-2, 0], [2, 0]], [self.x, self.y])
        ]
        self.objects = [
            Rock(32, 128)
        ]
        self.map = [[0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 5, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 4, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 5, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0]]


