import pygame
import core.ResourceManager as res

from core.Character import Character
from core.Vector2D import Vector2D
from core.Vector2D import EPSILON, Vector2D

compassClips = ['right', 'down', 'down', 'down', 'left', 'up', 'up', 'up']

class Player(Character):
    attack = 30
    defense = 20
    HP = 500
    xp = 0
    speed = 3
    velocity = [0, 0]
    isCollide = False
    lastVelocity = [0, 0]
    objectCollition = None
    hasChanged = True

    def __init__(self, game, position, name, animName):
        super().__init__(game)
        self.set_name(name)
        self.animName = animName
        self.loadAnimation(res.getAnimFile(self.animName))
        self.x, self.y = position
        self.width = 34
        self.height = 56
        self.timeStep = 100
        self.colliding = []
        self.currentClip = "stand_down"
        self.action = self.currentClip

    def move(self, vector: Vector2D):
        self.velocity = vector

    def update(self, deltaTime: float):
        super().update(deltaTime)
        direction = compassClips[self.heading.getCompass()]
        self.currentClip = ('stand_' if self.velocity.isZero() else '') + direction

    def collitions(self, rect: pygame.Rect):
        if self.get_rect().colliderect(rect) == 1:
            self.stop()

    # colisiones por listas de rectangulos
    def listCollitions(self, listRect: list):
        self.colliding = self.get_rect().collidelistall(listRect)
        if self.colliding != []:
            self.stop()

    def get_rect(self):
        return pygame.Rect((self.x, self.y + 24, 34, 32))

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=self.traductor.get(self.currentClip)
        )

