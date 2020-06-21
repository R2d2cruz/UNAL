import pygame

from .BaseCamera import BaseCamera
from ..Vector2D import Vector2D


class SimpleCamera(BaseCamera):
    def __init__(self, viewWidth, viewHeight, worldWidth, worldHeight):
        super().__init__()
        self.__worldRect = pygame.Rect(0, 0, worldWidth, worldHeight)
        self.target = None
        self.boundLeft = 0
        self.boundRight = -self.__worldRect.width
        self.boundTop = 0
        self.boundBottom = -self.__worldRect.height
        self.fixToView = False
        self.view = pygame.Rect(0, 0, viewWidth, viewHeight)
        self.__calculateBounds()

    def __calculateBounds(self):
        if self.fixToView:
            self.boundLeft = -int(self.view.width / 2)
            self.boundRight = -self.__worldRect.width + int(self.view.width / 2)
            self.boundTop = -int(self.view.height / 2)
            self.boundBottom = -self.__worldRect.height + int(self.view.height / 2)
        else:
            self.boundLeft = 0
            self.boundTop = 0
            self.boundRight = -self.__worldRect.width
            self.boundBottom = -self.__worldRect.height

    def follow(self, target):
        self.target = target

    def apply(self, pos):
        if type(pos) == pygame.Rect:
            return pos.move(self.view.topleft)
        elif type(pos) == Vector2D:
            return int(pos.x + self.view.x), int(pos.y + self.view.y)
        elif type(pos) == tuple or type(pos) == list:
            return int(pos[0] + self.view.x), int(pos[1] + self.view.y)

    def update(self, deltaTime: float):
        if self.target is not None:
            # calcular  la posicion topLeft de la camara
            self.offsetX = -int(self.target.x + (self.target.width / 2))
            self.offsetY = -int(self.target.y + (self.target.height / 2))

            # limitar el movimiento de la camara para que el foco no se salga del mapa
            self.offsetX = max(self.boundRight, min(self.boundLeft, self.offsetX))
            self.offsetY = max(self.boundBottom, min(self.boundTop, self.offsetY))

            # se mueve la camara a la posicion calculada en el centro de la ventanda
            self.view.x = self.offsetX + int(self.view.width / 2)
            self.view.y = self.offsetY + int(self.view.height / 2)

    def render(self, screen):
        # pintar el view de la camara
        rect = pygame.Rect(
            -self.offsetX - (self.view.width / 2),  # + self.view.x,
            -self.offsetY - (self.view.height / 2),  # + self.view.y,
            self.view.width,
            self.view.height)
        pygame.draw.rect(screen, (255, 0, 0), self.apply(rect), 1)
        pygame.draw.rect(screen, (0, 255, 0), self.apply(self.__worldRect), 1)
