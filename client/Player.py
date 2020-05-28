import pygame
import core.ResourceManager as res

from core.Character import Character


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

    def move(self, vector: [], isMoving: bool):
        if isMoving:
            self.velocity = vector
            if self.velocity[1] == 0:
                self.currentClip = "right" if self.velocity[0] > 0 else "left"
            else:
                self.currentClip = "down" if self.velocity[1] > 0 else "up"
        elif self.velocity != [0, 0]:
            if self.velocity[1] == 0:
                self.currentClip = "stand_right" if self.velocity[0] > 0 else "stand_left"
            else:
                self.currentClip = "stand_down" if self.velocity[1] > 0 else "stand_up"
            self.velocity = [0, 0]
        self.hasChanged = True

    # def move(self, direction):
    #     if direction == "up":
    #         self.velocity = [0, -1]
    #     if direction == "down":
    #         self.velocity = [0, 1]
    #     if direction == "right":
    #         self.velocity = [1, 0]
    #     if direction == "left":
    #         self.velocity = [-1, 0]
    #
    #     if direction == "stand_up":
    #         self.velocity = [0, 0]
    #     if direction == "stand_down":
    #         self.velocity = [0, 0]
    #     if direction == "stand_right":
    #         self.velocity = [0, 0]
    #     if direction == "stand_left":
    #         self.velocity = [0, 0]
    #
    #     self.currentClip = direction
    #     self.hasChanged = True

    def update(self, deltaTime: float):
        super().update(deltaTime)
        if self.lastVelocity != self.velocity:
            self.x += self.velocity[0] * self.speed
            self.y += self.velocity[1] * self.speed
        self.hasChanged = self.velocity != [0, 0]

    def collitions(self, rect: pygame.Rect):
        this = self.get_rect().copy()
        this.x += self.velocity[0] * self.speed
        this.y += self.velocity[1] * self.speed
        if this.colliderect(rect) == 1:
            self.move(self.velocity, False)
            self.velocity = [0, 0]

    # colisiones por listas de rectangulos
    def listCollitions(self, listRect: list):
        this = self.get_rect().copy()
        this.x += self.velocity[0] * self.speed
        this.y += self.velocity[1] * self.speed
        self.colliding = this.collidelistall(listRect)
        # print(self.colliding)
        if self.colliding != []:
            self.move(self.velocity, False)
            self.velocity = [0, 0]

    def get_rect(self):
        return pygame.Rect((self.x, self.y + 24, 34, 32))

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=self.traductor.get(self.currentClip)
        )

    # def prox_rect(self):
    #     x = self.rect.x + self.velocity[0]
    #     y = self.rect.y + self.velocity[1]
    #     return pygame.Rect((x, y, 34, 32))
