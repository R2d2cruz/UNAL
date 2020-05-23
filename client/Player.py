import pygame
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
    action = "stand_down"
    hasChanged = True

    def __init__(self, game, position, name):
        super().__init__(game)
        self.set_name(name)
        self.loadAnimation(game.res.getRandomCharAnimFile(), game.res)
        self.rect.topleft = position
        self.x = 100
        self.y = 100
        self.timeStep = 100

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
        # if self.action is not None:
        super().update(self.action)
        if self.lastVelocity != self.velocity:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        self.hasChanged = self.velocity != [0, 0]

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
