import pygame

from .BaseCamera import BaseCamera
from ..v2D import Vector2D


class SimpleCamera(BaseCamera):
    def __init__(self, viewWidth, viewHeight, worldWidth, worldHeight, fixedToView):
        super().__init__()
        self.__worldRect = pygame.Rect(0, 0, worldWidth, worldHeight)
        self.target = None
        self.view = pygame.Rect(0, 0, viewWidth, viewHeight)
        self.boundLeft = 0
        self.boundRight = -self.__worldRect.width
        self.boundTop = 0
        self.boundBottom = -self.__worldRect.height
        self.fixToView = fixedToView
        self.__calculateBounds()

    # @property
    # def bounds(self):
    #     if self.fixToView:
    #         return pygame.Rect(
    #             int(self.view.width / 2),
    #             int(self.view.height / 2),
    #             self.__worldRect.width - int(self.view.width / 2),
    #             self.__worldRect.height - int(self.view.height / 2))
    #     else:
    #         return pygame.Rect(0, 0, self.__worldRect.width, self.__worldRect.height)

    def __calculateBounds(self):
        if self.fixToView:
            self.boundLeft = -self.__worldRect.width + int(self.view.width / 2)
            self.boundRight = -int(self.view.width / 2)
            self.boundTop = -self.__worldRect.height + int(self.view.height / 2)
            self.boundBottom = -int(self.view.height / 2)
        else:
            self.boundLeft = -self.__worldRect.width
            self.boundRight = 0
            self.boundTop = -self.__worldRect.height
            self.boundBottom = 0

    def follow(self, target):
        self.target = target

    def apply(self, pos):
        if type(pos) == pygame.Rect:
            return pos.move(self.view.center)
        elif type(pos) == Vector2D:
            return int(pos.x + self.view.centerx), int(pos.y + self.view.centery)
        elif type(pos) == tuple or type(pos) == list:
            return int(pos[0] + self.view.centerx), int(pos[1] + self.view.centery)

    def unapply(self, pos):
        if type(pos) == pygame.Rect:
            return pos.move(-self.view.centerx, -self.view.centery)
        elif type(pos) == Vector2D:
            return int(pos.x - self.view.centerx), int(pos.y - self.view.centery)
        elif type(pos) == tuple or type(pos) == list:
            return int(pos[0] - self.view.centerx), int(pos[1] - self.view.centery)

    def update(self, deltaTime: float):
        if self.target is not None:
            # calcular  la posicion topLeft de la camara
            # offsetX = -int(self.target.x + (self.target.width / 2))
            offsetX = -int(self.target.centerx)
            # offsetY = -int(self.target.y + (self.target.height / 2))
            offsetY = -int(self.target.centery)

            # limitar el movimiento de la camara para que el foco no se salga del mapa
            # se mueve la camara a la posicion calculada en el centro de la ventanda
            if self.__worldRect.width < self.view.width:
                self.view.x = -self.__worldRect.width / 2
            else:
                self.view.x = max(self.boundLeft, min(self.boundRight, offsetX))

            if self.__worldRect.height < self.view.height:
                self.view.y = -self.__worldRect.height / 2
            else:
                self.view.y = max(self.boundTop, min(self.boundBottom, offsetY))

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.apply(self.view), 1)
        pygame.draw.rect(surface, (0, 255, 0), self.apply(self.__worldRect), 1)
