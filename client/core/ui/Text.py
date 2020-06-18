import pygame
from core.ui.Control import Control
from core.ResourceManager import blitMultiLineText
from core.camera.BaseCamera import BaseCamera


class Text(Control):
    def __init__(self, x, y, width, heigth, font, text='', foreColor=Control.WHITE):
        super().__init__(x, y, width, heigth)
        self.__surface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__padding = 10
        self.__isPressed = False
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__surface = pygame.Surface((self.rect.w, self.rect.h))
        self.__surface.fill((255, 255, 255))
        pygame.draw.rect(self.__surface, (128, 128, 128), (0, 0, self.rect.w, self.rect.h), 5)
        self.__textRect = pygame.Rect(
            self.__padding,
            self.__padding,
            self.rect.w - (self.__padding * 2),
            self.rect.h - (self.__padding * 2))
        blitMultiLineText(self.__surface, text, self.__textRect, self.__font)

    def onRender(self, screen, camera: BaseCamera):
        screen.blit(self.__surface, self.rect)