import pygame
import core.ResourceManager as res

from core.Character import Character
from core.Vector2D import Vector2D
from core.Vector2D import EPSILON, Vector2D


class Player(Character):
    attack = 30
    defense = 20
    HP = 500
    xp = 0

    def __init__(self, name, animationName, position):
        super().__init__(name, animationName, position)

    def move(self, vector: Vector2D):
        self.velocity = vector

    def collitions(self, rect: pygame.Rect):
        if self.get_rect().colliderect(rect) == 1:
            self.stop()

    # colisiones por listas de rectangulos
    def listCollitions(self, listRect: list):
        colliding = self.get_rect().collidelistall(listRect)
        if colliding != []:
            self.stop()

    def get_rect(self):
        return pygame.Rect((self.x, self.y + 24, 34, 32))

