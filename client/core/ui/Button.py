import pygame
from core.ui.Control import Control
from core.ResourceManager import getText


class Button(Control):

    def __init__(self, x, y, width, heigth, font, text='', foreColor = Control.WHITE):
        super().__init__(x, y, width, heigth)
        self.__surface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__isPressed = False
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__surface, self.__textRect = getText(self.__text, self.__font, self.__color)
        self.__textRect.x = 2 + self.rect.x + (self.rect.w - self.__surface.get_width()) / 2
        self.__textRect.y = 2 + self.rect.y + (self.rect.h - self.__surface.get_height()) / 2

    def render(self, screen):
        screen.fill((123, 123, 123), self.rect)

        if self.__isPressed:
            screen.blit(self.__surface, self.__textRect.move(1 , 2))
        else:
            screen.blit(self.__surface, self.__textRect)

        pygame.draw.rect(screen, self.COLOR_INACTIVE, self.rect, 3)

    def onMouseUp(self, event):
        self.__isPressed = False
        self.onClick(self)

    def onMouseDown(self, event):
        self.__isPressed = True

    def onClick(self, sender):
        pass