import pygame
from core.Telegram import Telegram


class Entity(pygame.sprite.Sprite):

    __nextID = 0

    def __init__(self, *groups):
        super().__init__()
        self.image = None
        self.name = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.flag = ""
        self.__id = self.getMyId()
        self.__onMessages = False
        self.handelMessages = self.offHandleMessages

    @property
    def onMessage(self):
        return self.__onMessages

    def switchMessage(self):
        self.__onMessages = not self.__onMessages
        if self.__onMessages:
            self.handelMessages = self.onHandleMessages
        else:
            self.handelMessages = self.offHandleMessages

    @staticmethod
    def getMyId():
        newId = Entity.__nextID
        Entity.__nextID += 1
        return newId

    @property
    def id(self):
        return self.__id

    @property
    def x(self):
        return self.rect.left

    @x.setter
    def x(self, x):
        self.rect.left = x

    @property
    def y(self):
        return self.rect.top

    @y.setter
    def y(self, y):
        self.rect.top = y

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
    def height(self, height):
        self.rect.height = height

    def getCollisionRect(self):
        return self.rect

    def getOldCollisionRect(self):
        return self.rect

    def update(self, deltaTime: float):
        pass

    def render(self, screen, camera=None):
        if camera is None:
            screen.blit(self.image, self.rect)
            # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        else:
            screen.blit(self.image, camera.apply(self.rect))
            pygame.draw.rect(screen, (0, 0, 255), camera.apply(self.rect), 1)
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.getCollisionRect()), 1)

    def dispose(self):
        pass

    def handelMessages(self, telegram: Telegram):
        pass

    def onHandleMessages(self, telegram: Telegram):
        pass

    def offHandleMessages(self, telegram: Telegram):
        pass
