import pygame

from .core import Character, Vector2D


class Player(Character):

    def __init__(self, name, animationName, position, collisionRect):
        super().__init__(name, animationName, position, collisionRect)
        self.health = 20
        self.xp = 0

    def move(self, vector: Vector2D):
        self.velocity = vector

    def collitions(self, rect: pygame.Rect):
        collideRect = self.get_rect()
        if collideRect.colliderect(rect) == 1:
            self.stop(collideRect.x + collideRect.w >= rect.x or collideRect.x >= rect.x + rect.w)

    # colisiones por listas de rectangulos
    def listCollitions(self, listRect: list):
        collideRect = self.get_rect()
        colliding = collideRect.collidelistall(listRect)
        if colliding != []:
            for i in colliding:
                if listRect[i].flag == "item":
                    if listRect[i].effect(self):
                        listRect.pop(i)
                else:
                    self.stop(collideRect.x + collideRect.w >= listRect[i].x or
                              collideRect.x >= listRect[i].x + listRect[i].w)
