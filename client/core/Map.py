import json
import pygame
from copy import copy

import os

if os.name != "nt":
    from OnlinePlayers import OnlinePlayer
    from Objects import Wall
else:
    from client.OnlinePlayers import OnlinePlayer
    from client.Objects import Wall


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

    player = None
    players = {}
    x = 0
    y = 0
    rect = 32

    def __init__(self, game):
        self.game = game

    def loadMap(self, fileName):
        map = []
        with open(fileName) as json_file:
            data = json.load(json_file)
            for row in data:
                newRow = []
                for col in row:
                    newRow.append(col)
                map.append(newRow)
            return map

    def loadFrames(self, fileName):
        frames = {}
        with open(fileName) as json_file:
            data = json.load(json_file)
            if os.name != "nt":
                image = pygame.image.load(data.get("image"))
            else:
                image = pygame.image.load("../" + data.get("image"))
            for frame in data.get("tiles"):
                frames[frame["id"]] = image.subsurface(frame["box"])
        return frames

    def createWalls(self, fileName):
        objects = self.loadMap(fileName)
        real_objects = []
        for i in range(len(objects)):
            for j in range(len(objects[i])):
                if objects[i][j] == 1:
                    x = j * 32
                    y = i * 32
                    obj = Wall(x, y)
                    real_objects.append(copy(obj))
        return real_objects

    def changeCoord(self, x, y):
        self.x = x
        self.y = y
        for i in self.characters:
            i.change_reference_point([self.x, self.y])
        for i in self.objects:
            i.change_reference_point([self.x, self.y])
        for i in self.players.keys():
            self.players[i].change_reference_point([self.x, self.y])

    def updateOtherPlayers(self):
        message = self.game.client.getStatus()
        information = json.loads(message)
        # print(information)
        keys = self.players.keys()
        for i in information.keys():
            if i in keys:
                self.players.get(i).setPos(information.get(i))
            else:
                self.players[i] = OnlinePlayer(information.get(i))
            self.changeCoord(self.player.get_x(), self.player.get_y())

    def update(self):
        self.collitions()
        if self.player.hasChanged:
            self.player.hasChanged = False
            self.game.client.sendPlayerStatus(self.player)
        self.updateOtherPlayers()
        for i in self.players.keys():
            self.players.get(i).update()
        for char in self.characters:
            char.update()
            char.update()
        for obj in self.objects:
            obj.update()
            self.player.collitions(obj)
        self.player.update()
        if self.player.hasChanged:
            self.changeCoord(self.player.get_x(), self.player.get_y())

    def blit(self, screen):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                screen.blit(self.frames.get(self.map[i][j]), (self.x + (self.rect * j), self.y + (self.rect * i)))
        for k in self.characters:
            k.render(screen)
        for k in self.objects:
            k.render(screen)
        for k in self.players.values():
            k.render(screen)
        self.player.render(screen)

    def collitions(self):
        for i in range(len(self.characters)):
            self.player.collitions(self.characters[i])
            self.characters[i].collitions(self.player)
