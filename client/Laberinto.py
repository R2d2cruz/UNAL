import json
from copy import copy

from core import (AnimatedEntity, Graph, Map, Vector2D, collisionManager,
                  entityManager, resourceManager)
from Item import HealthPotion
from Objects import Wall


class Laberinto(Map):
    def __init__(self):
        super().__init__()
        self.frames = self.loadTileset(resourceManager.getTileset("ts1"))
        mapName = 'laberinto'
        self.objects = self.createWalls(resourceManager.getMap(mapName))
        self.cells = self.loadMap(resourceManager.getMap(mapName)) 
        self.graph = Graph()
        self.graph.nodes = Graph.getGraph(self, True)
        with open('saves/' + mapName + '.graph.json', 'w') as outfile:
            json.dump(self.graph.nodes, outfile)
        potion = HealthPotion("freshPotion", (3, 2, 10, 12), Vector2D(160, 288), 20)
        self.objects.append(potion)
        collisionManager.registerEntity(potion)

        for i in range(1, 10):
            fire = AnimatedEntity()
            fire.loadAnimation(resourceManager.getAnimFile("fire"))
            fire.x = 50 * i
            fire.y = 0
            self.objects.append(fire)
        entityManager.registerEntities(self.objects)

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
