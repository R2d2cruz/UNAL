import pygame


class Control:

    WHITE = (255, 255, 255)
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')

    def __init__(self, x, y, width, height):
        self.__active = False
        self.__hovered = False
        self.rect = pygame.Rect(x, y, width, height)

    @property
    def isActive(self):
        return self.__active

    def update(self):
        pass

    def render(self, screen):
        pass

    def handleEvent(self, event):
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
