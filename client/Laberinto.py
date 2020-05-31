import core.ResourceManager as res

from copy import copy
from core.Map import Map
from core.AnimatedEntity import AnimatedEntity
from Objects import Wall
from Item import HealthPotion
from core.Vector2D import Vector2D
from core.CollisionManager import collisionManager

class Laberinto(Map):
    def __init__(self):
        super().__init__()
        self.frames = self.loadTileset(res.getTileset("ts1"))
        self.objects = self.createWalls(res.getMap("empty"))
        self.map = self.loadMap(res.getMap("empty"))
        self.objects.append(HealthPotion("freshPotion", (3, 2, 10, 12), Vector2D(160, 288), 20))

        for i in range(1, 10):
            fire = AnimatedEntity()
            fire.loadAnimation(res.getAnimFile("fire"))
            fire.x = 50 * i
            fire.y = 0
            self.objects.append(fire)

    def createWalls(self, fileName: str):
        objects = self.loadMap(fileName)
        real_objects = []
        for i in range(len(objects)):
            for j in range(len(objects[i])):
                if objects[i][j] == 1:
                    x = j * 32
                    y = i * 32
                    obj = Wall(x, y)
                    real_objects.append(copy(obj))
                    collisionManager.registerEntity(obj) # las paredes no deberian ser objetos... o si?
        return real_objects
