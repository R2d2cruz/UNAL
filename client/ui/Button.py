import pygame

from .gui import gui
from .Control import Control
from ..core.camera import BaseCamera
from ..core.misc import getText


class Button(Control):
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font, text: str = '',
                 foreColor=Control.WHITE):
        super().__init__(x, y, width, height)
        self.__surface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__isPressed = False
        self.text = text
        self.backColor = (123, 123, 123)

    def refresh(self):
        self.__textRect.x = 2 + self.rect.x + (self.rect.w - self.__surface.get_width()) / 2
        self.__textRect.y = 2 + self.rect.y + (self.rect.h - self.__surface.get_height()) / 2

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__surface, self.__textRect = getText(self.__text, self.__font, self.__color)
        self.refresh()

    def onRender(self, surface, camera: BaseCamera):
        # surface.fill(self.backColor, self.rect)
        if not self.isEnabled():
            skinElement = 'button-disabled'
        elif self.__isPressed:
            skinElement = 'button-pressed'
        elif self.isHovered():
            skinElement = 'button-active'
        elif self.isActive():
            skinElement = 'button-active'
        else:
            skinElement = 'button'
        gui.renderElement(surface, self.rect, skinElement)
        surface.blit(self.__surface, self.__textRect)
        # pygame.draw.rect(surface, self.COLOR_INACTIVE, self.rect, 3)

    def onMouseUp(self, event):
        self.__isPressed = False
        self.onClick(self)

    def onMouseDown(self, event):
        self.__isPressed = True

    def onClick(self, sender):
        pass
