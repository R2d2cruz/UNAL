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
        self.__hovered = False
        self.parent = None
        self.zIndex = 0
        self.tag = None
        self.name = 'Control' + str(self.__id)
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
        self.refresh()

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y
        self.refresh()

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

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.rect.width = width
        self.refresh()

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height: int):
        self.rect.height = height
        self.refresh()

    def refresh(self):
        pass

    def show(self):
        self.__visible = True

    def hide(self):
        self.__visible = False

    def isVisible(self) -> bool:
        return self.__visible

    def setActive(self):
        if self.parent is not None:
            self.parent.setActiveControl(self)

    def setInactive(self):
        if self.parent is not None and self == self.parent.activeControl:
            self.parent.setActiveControl(None)

    def isActive(self) -> bool:
        if self.parent is not None:
            return self == self.parent.activeControl
        return False

    def isHovered(self) -> bool:
        return self.__hovered

    def enable(self):
        self.__enabled = True

    def disable(self):
        self.__enabled = False

    def isEnabled(self) -> bool:
        return self.__enabled

    def update(self, deltaTime: float):
        pass

    def render(self, surface, camera: BaseCamera):
        if self.__visible:
            self.onRender(surface, camera)

    def handleKeyEvent(self, event) -> bool:
        if event.type == pygame.KEYDOWN:
            if self.isActive():
                return self.onKeyDown(event, self)
        return False

    def handleMouseEvent(self, event) -> bool:
        if (not self.__visible) or (not self.__enabled):
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(self.name, self.isActive(), 'MOUSEBUTTONDOWN')
            if self.rect.collidepoint(event.pos):
                self.setActive()
                self.onMouseDown(event, self)
                return True
            else:
                self.setInactive()
        elif event.type == pygame.MOUSEBUTTONUP:
            # print(self.name, self.isActive(), 'MOUSEBUTTONUP')
            if self.rect.collidepoint(event.pos):
                if self.isActive():
                    self.onMouseUp(event, self)
                return True
            else:
                self.setInactive()
        elif event.type == pygame.MOUSEMOTION:
            # print(self.name, self.isActive(), 'MOUSEMOTION')
            if self.rect.collidepoint(event.pos):
                if not self.__hovered:
                    self.onMouseEnter(event, self)
                self.__hovered = True
                # self.onMouseMove(event, self)
                return True
            else:
                if self.__hovered:
                    self.onMouseLeave(event, self)
                self.__hovered = False
        return False

    def onRender(self, surface, camera):
        pass

    def onMouseUp(self, event, sender):
        pass

    def onMouseDown(self, event, sender):
        pass

    def onMouseEnter(self, event, sender):
        pass

    def onMouseMove(self, event, sender):
        pass

    def onMouseLeave(self, event, sender):
        pass

    def onKeyDown(self, event, sender) -> bool:
        return False

    def onKeyUp(self, event, sender) -> bool:
        return False
