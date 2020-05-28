import pygame
import core.ResourceManager as res

from core.Entity import Entity


class Rock(Entity):
    def __init__(self, game, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = res.loadImage("ts1", (64, 32, 32, 32))


class Three(Entity):
    def __init__(self, game, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = res.loadImage("ts1", (0, 0, 32, 64))


class Wall(Entity):
    def __init__(self, game, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = res.loadImage("ts1", (96, 64, 32, 32))
