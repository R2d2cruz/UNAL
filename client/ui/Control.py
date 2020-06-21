import pygame

from ..core import BaseCamera


class Control:
    __nextID = 0

    WHITE = (255, 255, 255)
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')

    def __init__(self, x: int, y: int, width: int, height: int):
        self.__id = self.__getNextID()
        self.__visible = True
        self.__enabled = True
        self.__active = False
        self.__hovered = False
        self.tag = None
        self.rect = pygame.Rect(x, y, width, height)

    @staticmethod
    def __getNextID():
        newId = Control.__nextID
        Control.__nextID += 1
        return newId

    @property
    def id(self):
        return self.__id

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x
        self.__refresh()

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y
        self.__refresh()

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.rect.width = width
        self.__refresh()

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height: int):
        self.rect.height = height
        self.__refresh()

    def __refresh(self):
        pass

    def show(self):
        self.__visible = True

    def hide(self):
        self.__visible = False

    def isVisible(self) -> bool:
        return self.__visible

    def enable(self):
        self.__enabled = True

    def disable(self):
        self.__enabled = False

    def isEnabled(self) -> bool:
        return self.__enabled

    def update(self, deltaTime: float):
        pass

    def render(self, screen, camera: BaseCamera):
        if self.__visible:
            self.onRender(screen, camera)

    def handleEvent(self, event):
        if (not self.__visible) or (not self.__enabled):
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.__active = True
                self.onMouseDown(event)
            else:
                self.__active = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                if self.__active:
                    self.onMouseUp(event)
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if not self.__hovered:
                    self.onMouseEnter(event)
                self.__hovered = True
            else:
                if self.__hovered:
                    self.onMouseLeave(event)
                self.__hovered = False
        elif event.type == pygame.KEYDOWN:
            if self.__active:
                self.onKeyDown(event)

    def onRender(self, screen, camera):
        pass

    def onMouseUp(self, event):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseEnter(self, event):
        pass

    def onMouseLeave(self, event):
        pass

    def onKeyDown(self, event):
        pass

    def onKeyUp(self, event):
        pass
