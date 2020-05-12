import os

if os.name != "nt":
    from constants import imgsOS as imgs, mapsOS as maps, tilesetsOS as tilesets
    from Player import Player
    from core.Map import Map
else:
    from client.constants import imgsNT as imgs, mapsNT as maps, tilesetsNT as tilesets
    from client.Player import Player
    from client.core.Map import Map


class Laberinto(Map):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player((640, 360))
        self.x = self.player.get_x()
        self.y = self.player.get_y()
        self.frames = self.loadFrames(tilesets.get("ts1"))
        self.objects = self.createWalls(maps.get("walls"))
        self.map = self.loadMap(maps.get("laberinto"))
