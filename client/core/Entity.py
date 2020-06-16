import pygame
from core.Vector2D import Vector2D
from core.Telegram import Telegram
from core.camera.BaseCamera import BaseCamera


class Entity(pygame.sprite.Sprite):

    __nextID = 0

    def __init__(self, *groups):
        super().__init__()
        self.__pos = Vector2D(0, 0)
        self.__id = self.getMyId()
        self.image = None
        self.name = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.flag = ""
        self.script = None

    @staticmethod
    def getMyId():
        newId = Entity.__nextID
        Entity.__nextID += 1
        print('Nueva entidad con ID', newId)
        return newId

    @property
    def id(self):
        return self.__id

    @property
    def x(self):
        return self.__pos.x

    @x.setter
    def x(self, x):
        self.__pos.x = x

    @property
    def y(self):
        return self.__pos.y

    @y.setter
    def y(self, y):
        self.__pos.y = y

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.rect.width = width

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height: int):
        self.rect.height = height

    def getCollisionRect(self):
        return self.rect

    def getOldCollisionRect(self):
        return self.rect

    def update(self, deltaTime: float):
        if self.script is not None:
            self.script.onUpdate(self)

    def render(self, screen, camera: BaseCamera):
        screen.blit(self.image, camera.apply(self.rect))
        #pygame.draw.rect(screen, (0, 0, 255), camera.apply(self.rect), 1)
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.getCollisionRect()), 1)

    def dispose(self):
        pass

    def onMessage(self, telegram: Telegram) -> bool:
        pass
