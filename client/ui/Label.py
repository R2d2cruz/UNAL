import pygame

from .Control import Control
from ..core import BaseCamera
from ..core.misc import getText


class Label(Control):
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font, text='',
                 foreColor=Control.WHITE):
        super().__init__(x, y, width, height)
        self.__surface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__padding = 5
        self.__isPressed = False
        self.text = text

    def _Control__refresh(self):
        self.__textRect.x = self.rect.x + self.__padding
        self.__textRect.y = self.rect.y + (self.rect.h - self.__surface.get_height()) / 2

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__surface, self.__textRect = getText(self.__text, self.__font, self.__color)
        self._Control__refresh()

    def onRender(self, screen, camera: BaseCamera):
        screen.blit(self.__surface, self.__textRect)
