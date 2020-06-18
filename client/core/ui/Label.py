import pygame
from core.ui.Control import Control
from core.ResourceManager import getText
from core.camera.BaseCamera import BaseCamera


class Label(Control):
    def __init__(self, x, y, width, heigth, font, text='', foreColor=Control.WHITE):
        super().__init__(x, y, width, heigth)
        self.__surface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__padding = 5
        self.__isPressed = False
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__surface, self.__textRect = getText(self.__text, self.__font, self.__color)
        self.__textRect.x = self.rect.x + self.__padding
        self.__textRect.y = self.rect.y + (self.rect.h - self.__surface.get_height()) / 2

    def onRender(self, screen, camera: BaseCamera):
        screen.blit(self.__surface, self.__textRect)
