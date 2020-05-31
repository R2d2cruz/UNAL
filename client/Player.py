import pygame
import core.ResourceManager as res

from core.Character import Character
from core.Vector2D import Vector2D
from core.Vector2D import EPSILON, Vector2D


class Player(Character):

    def __init__(self, name, animationName, position):
        super().__init__(name, animationName, position)
        self.health = 20
        self.xp = 0

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
            for i in colliding:
                if listRect[i].flag == "item":
                    if listRect[i].effect(self):
                        listRect.pop(i)

