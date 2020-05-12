import json
import pygame
import os

if os.name != "nt":
    from constants import imgsOS as imgs
    from core.Character import Character
else:
    from client.constants import imgsNT as imgs
    from client.core.Character import Character


class Player(Character):
    attack = 30
    defense = 20
    HP = 500
    x = 100
    y = 100
    xp = 0
    speed = 3
    velocity = [0, 0]
    isCollide = False
    lastVelocity = [0, 0]
    objectCollition = None
    action = "stand_down"
    hasChanged = False

    def __init__(self, position, name="Henry"):
        super().__init__()
        self.name = name
        self.loadImg(imgs.get(self.name))
        self.rect.topleft = position
        self.frame = 0
        self.front = {0: (37, 1, 34, 56)}
        self.back = {0: (1, 1, 34, 56)}
        self.left = {0: (217, 1, 32, 56)}
        self.right = {0: (251, 1, 32, 56)}
        self.walk = {0: (357, 1, 34, 53), 1: (37, 1, 34, 56), 2: (393, 1, 34, 53), 3: (37, 1, 34, 56)}
        self.backWalk = {0: (285, 1, 34, 54), 1: (1, 1, 34, 56), 2: (321, 1, 34, 54), 3: (1, 1, 34, 56)}
        self.leftWalk = {0: (109, 1, 34, 56), 1: (217, 1, 32, 56), 2: (181, 1, 34, 56), 3: (217, 1, 32, 56)}
        self.rightWalk = {0: (73, 1, 34, 56), 1: (251, 1, 32, 56), 2: (145, 1, 34, 56), 3: (251, 1, 32, 56)}

    def move(self, direction):
        if direction == "up":
            self.velocity = [0, 4]
            self.clip(self.backWalk)
        if direction == "down":
            self.velocity = [0, -4]
            self.clip(self.walk)
        if direction == "right":
            self.velocity = [-4, 0]
            self.clip(self.rightWalk)
        if direction == "left":
            self.velocity = [4, 0]
            self.clip(self.leftWalk)

        if direction == "stand_up":
            self.velocity = [0, 0]
            self.clip(self.back)
        if direction == "stand_down":
            self.velocity = [0, 0]
            self.clip(self.front)
        if direction == "stand_right":
            self.velocity = [0, 0]
            self.clip(self.right)
        if direction == "stand_left":
            self.velocity = [0, 0]
            self.clip(self.left)

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.action = direction
        self.hasChanged = True

    def update(self):
        if self.lastVelocity != self.velocity:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        if self.velocity == [0, 0]:
            self.hasChanged = False
        # return self.velocity == [0, 0]

    def collitions(self, object):
        this = self.get_rect().copy()
        this.x -= self.velocity[0]
        this.y -= self.velocity[1]
        if this.colliderect(object) == 1:
            self.velocity = [0, 0]

    def get_rect(self):
        return pygame.Rect((self.rect.x, self.rect.y + 24, 34, 32))

    def prox_rect(self):
        x = self.rect.x + self.velocity[0]
        y = self.rect.y + self.velocity[1]
        return pygame.Rect((x, y, 34, 32))