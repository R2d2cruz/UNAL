import pygame

from .BaseCamera import BaseCamera
from ..Vector2D import Vector2D


class SimpleCamera(BaseCamera):
    def __init__(self, viewWidth, viewHeight, worldWidth, worldHeight):
        super().__init__()
        self.__worldRect = pygame.Rect(0, 0, worldWidth, worldHeight)
        self.__view = pygame.Rect(0, 0, viewWidth, viewHeight)
        self.__target = None
        self.boundLeft = 0
        self.boundRight = -self.__worldRect.width
        self.boundTop = 0
        self.boundBottom = -self.__worldRect.height
        self.fixToView = False
        self.__calculateBounds()

    def __calculateBounds(self):
        if self.fixToView:
            self.boundLeft = -self.__worldRect.width + int(self.__view.width / 2)
            self.boundRight = -int(self.__view.width / 2)
            self.boundTop = -self.__worldRect.height + int(self.__view.height / 2)
            self.boundBottom = -int(self.__view.height / 2)
        else:
            self.boundLeft = -self.__worldRect.width
            self.boundRight = 0
            self.boundTop = -self.__worldRect.height
            self.boundBottom = 0

    def follow(self, target):
        self.__target = target

    def apply(self, pos):
        if type(pos) == pygame.Rect:
            return pos.move(self.__view.center)
        elif type(pos) == Vector2D:
            return int(pos.x + self.__view.centerx), int(pos.y + self.__view.centery)
        elif type(pos) == tuple or type(pos) == list:
            return int(pos[0] + self.__view.centerx), int(pos[1] + self.__view.centery)

    def unapply(self, pos):
        if type(pos) == pygame.Rect:
            return pos.move(-self.__view.centerx, -self.__view.centery)
        elif type(pos) == Vector2D:
            return int(pos.x - self.__view.centerx), int(pos.y - self.__view.centery)
        elif type(pos) == tuple or type(pos) == list:
            return int(pos[0] - self.__view.centerx), int(pos[1] - self.__view.centery)

    def update(self, deltaTime: float):
        if self.__target is not None:
            # calcular  la posicion topLeft de la camara
            offsetX = -int(self.__target.x + (self.__target.width / 2))
            offsetY = -int(self.__target.y + (self.__target.height / 2))

            # limitar el movimiento de la camara para que el foco no se salga del mapa
            # se mueve la camara a la posicion calculada en el centro de la ventanda
            self.__view.x = max(self.boundLeft, min(self.boundRight, offsetX))
            self.__view.y = max(self.boundTop, min(self.boundBottom, offsetY))

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.apply(self.__view), 1)
        pygame.draw.rect(surface, (0, 255, 0), self.apply(self.__worldRect), 1)
