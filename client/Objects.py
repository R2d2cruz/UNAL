import pygame
import os
if os.name != "nt":
    from constants import imgsOS as imgs
else:
    from client.constants import imgsNT as imgs

from core.Entity import Entity

class Rock(Entity):
    def __init__(self, x, y):
        super().__init__(*groups)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.x = x
        self.y = y
        image = pygame.image.load(imgs.get("ts1"))
        self.image = image.subsurface((64, 32, 32, 32))

class Three(Entity):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.x = x
        self.y = y
        image = pygame.image.load(imgs.get("ts1"))
        self.image = image.subsurface((0, 0, 32, 64))

class Wall(Entity):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.x = x
        self.y = y
        image = pygame.image.load(imgs.get("ts1"))
        self.image = image.subsurface((96, 64, 32, 32))
