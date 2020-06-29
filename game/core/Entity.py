import pygame

from .Telegram import Telegram
from .v2D import Vector2D
from .camera.BaseCamera import BaseCamera
from .misc import Colors


class Entity(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__()
        self.__pos = Vector2D(0, 0)
        self.type = "entity"
        self.image = None
        self.name = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.tag = False
        self.script = None
        self.cellIndex = None
        self.selected = False
        self.wrapper = None
        self.data = {}
        self.tangible = True

    def __repr__(self):
        return f'[{self.id}: {self.name}: {self.type}: {self.__pos}]'

    @property
    def getMe(self):
        return dict(
            position=self.getPos(),
            collisionRect=self.getCollisionRect(),
            id=self.id,
            type=self.type
        )

    @property
    def id(self):
        return id(self)

    @property
    def x(self):
        return self.__pos.x

    @x.setter
    def x(self, x):
        self.__pos.x = x
        self.rect.left = x

    @property
    def y(self):
        return self.__pos.y

    @y.setter
    def y(self, y):
        self.__pos.y = y
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
    def height(self, height: int):
        self.rect.height = height

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, top):
        self.rect.top = top
        self.refresh()

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, left):
        self.rect.left = left
        self.refresh()

    @property
    def right(self):
        return self.rect.right

    @right.setter
    def right(self, right):
        self.rect.right = right
        self.refresh()

    @property
    def bottom(self):
        return self.rect.bottom

    @bottom.setter
    def bottom(self, bottom):
        self.rect.right = bottom
        self.refresh()

    @property
    def centerx(self):
        return self.rect.centerx

    @centerx.setter
    def centerx(self, centerx):
        self.rect.centerx = centerx
        self.refresh()

    @property
    def centery(self):
        return self.rect.centery

    @centery.setter
    def centery(self, centery):
        self.rect.centery = centery
        self.refresh()

    def radius(self):
        return (self.rect.width / 2) * 1.4142

    def setPos(self, x: float, y: float):
        self.x, self.y = x, y

    def getPos(self):
        return self.__pos

    # se agrega esta funcion para evitar un error, sin embargo no 
    # pertenece a esta clase y deberia ser eliminada en el futuro
    def getOldPos(self):
        return self.__pos

    def getCollisionRect(self) -> pygame.Rect:
        return self.rect

    def getOldCollisionRect(self) -> pygame.Rect:
        return self.rect

    def getSelectionRect(self) -> pygame.Rect:
        return self.rect

    def update(self, deltaTime: float):
        pass

    def refresh(self):
        pass

    def render(self, surface, camera: BaseCamera):
        surface.blit(self.image, camera.apply(self.rect))
        # pygame.draw.rect(surface, Colors.GREEN, camera.apply(self.getCollisionRect()), 1)
        # if self.tag:
        #     pygame.draw.rect(surface, Colors.RED, camera.apply(self.getCollisionRect()), 4)
        if self.selected:
            pygame.draw.rect(surface, Colors.GREEN, camera.apply(self.rect), 4)
        # # else:
        #     pygame.draw.rect(surface, Colors.BLACK, camera.apply(self.getCollisionRect()), 1)
        pygame.draw.circle(surface, Colors.BLACK, camera.apply((self.x, self.y)), self.radius(), 1)

    def dispose(self):
        pass

    def onMessage(self, telegram: Telegram) -> bool:
        pass
