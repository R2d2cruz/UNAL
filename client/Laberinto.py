from Player import Player
from core.Game import Game
from core.Map import Map
from core.AnimatedEntity import AnimatedEntity


class Laberinto(Map):
    def __init__(self, game: Game):
        super().__init__(game)
        self.player = Player(game, (640, 360), '')
        self.x = self.player.get_x()
        self.y = self.player.get_y()
        self.frames = self.loadTileset(game.res.getTileset("ts1"), game.res)
        self.objects = self.createWalls(game.res.getMap("walls"))
        self.map = self.loadMap(game.res.getMap("laberinto"))

        for i in range(1, 10):
            fire = AnimatedEntity()
            fire.loadAnimation(game.res.getAnimFile("fire"), game.res)
            fire.x = 50 * i
            fire.y = 0
            self.objects.append(fire)

        self.changeCoord(self.player.get_x(), self.player.get_y())
