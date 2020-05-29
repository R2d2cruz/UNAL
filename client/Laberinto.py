import core.ResourceManager as res

from copy import copy
from core.Game import Game
from core.Map import Map
from core.AnimatedEntity import AnimatedEntity
from core.Character import Character
from Objects import Wall


class Laberinto(Map):
    def __init__(self, game: Game):
        super().__init__(game)
        self.frames = self.loadTileset(res.getTileset("ts1"))
        self.objects = self.createWalls(res.getMap("walls"))
        self.map = self.loadMap(res.getMap("laberinto"))

        for i in range(1, 10):
            fire = AnimatedEntity()
            fire.loadAnimation(res.getAnimFile("fire"))
            fire.x = 50 * i
            fire.y = 0
            self.objects.append(fire)

        for i in range(1, 5):
            name = res.getRandomCharAnimName()
            character = Character(name, name, (320 * i, 320 * i))
            self.characters.append(character)

    def render(self, screen, camera):
        super().render(screen, camera)
        for k in self.characters:
            k.render(screen, camera)

    def createWalls(self, fileName: str):
        objects = self.loadMap(fileName)
        real_objects = []
        for i in range(len(objects)):
            for j in range(len(objects[i])):
                if objects[i][j] == 1:
                    x = j * 32
                    y = i * 32
                    obj = Wall(self.game, x, y)
                    real_objects.append(copy(obj))
        return real_objects
