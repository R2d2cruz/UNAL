from Player import Player
from core.Map import Map
from Wanders import Wander
from Objects import *

from constants import imgs, maps

class UniversityMap(Map):
    def __init__(self):
        self.player = Player((640, 360))
        self.x = self.player.get_x()
        self.y = self.player.get_y()
        self.frames = self.loadFrames(tilesets.get("university"))
        self.map = self.loadMap(maps.get("university"))
        self.characters = [
            Wander((20, 0), [[0, 0], [200, 0]], [[-2, 0], [2, 0]], [self.x, self.y])
        ]
        self.objects = [
            Rock(32, 128)
        ]


