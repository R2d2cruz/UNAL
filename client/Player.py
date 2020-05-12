import json
import pygame
import os

if os.name != "nt":
    # noinspection PyUnresolvedReferences
    from constants import imgsOS as imgs, animsOS as anims
    # noinspection PyUnresolvedReferences
    from core.Character import Character
else:
    from client.constants import imgsNT as imgs, animsNT as anims
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
        self.loadSpriteAnimation(anims.get(self.name))
        self.rect.topleft = position

    def move(self, direction):
        if direction == "up":
            self.velocity = [0, 4]
        if direction == "down":
            self.velocity = [0, -4]
        if direction == "right":
            self.velocity = [-4, 0]
        if direction == "left":
            self.velocity = [4, 0]

        if direction == "stand_up":
            self.velocity = [0, 0]
        if direction == "stand_down":
            self.velocity = [0, 0]
        if direction == "stand_right":
            self.velocity = [0, 0]
        if direction == "stand_left":
            self.velocity = [0, 0]

        self.action = direction
        self.hasChanged = True

    def update(self):
        if self.action is not None:
            self.clip(self.action)
        if self.lastVelocity != self.velocity:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        if self.velocity == [0, 0]:
            self.hasChanged = False

    def collitions(self, obj):
        this = self.get_rect().copy()
        this.x -= self.velocity[0]
        this.y -= self.velocity[1]
        if this.colliderect(obj) == 1:
            self.velocity = [0, 0]

    def get_rect(self):
        return pygame.Rect((self.rect.x, self.rect.y + 24, 34, 32))

    def prox_rect(self):
        x = self.rect.x + self.velocity[0]
        y = self.rect.y + self.velocity[1]
        return pygame.Rect((x, y, 34, 32))
