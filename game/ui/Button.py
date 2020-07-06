import pygame

from .Control import Control
from .gui import gui
from ..core.camera import BaseCamera
from ..core.misc import getText


class Button(Control):
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font, text: str = '',
                 foreColor=Control.WHITE):
        super().__init__(x, y, width, height)
        self.__textSurface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__pressed = False
        self.skinElement = 'button'
        self.text = text
        self.backColor = (123, 123, 123)

    # def refresh(self):
    #     self.__textSurface, self.__textRect = getText(self.__text, self.__font, gui.skin['']['top-left'])
    #     if self.text is not None:
    #         self.__textRect.x = 2 + self.rect.x + (self.rect.w - self.__textSurface.get_width()) / 2
    #         self.__textRect.y = 2 + self.rect.y + (self.rect.h - self.__textSurface.get_height()) / 2

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.refresh()

    # @Control.active.setter
    # def active(self, active):
    #     self._Control__active = active
    #     self.__pressed = False

    def isPressed(self) -> bool:
        return self.__pressed

    @property
    def pressed(self):
        return self.__pressed

    @pressed.setter
    def pressed(self, pressed):
        self.__pressed = pressed

    def onRender(self, surface, camera: BaseCamera):
        # surface.fill(self.backColor, self.rect)
        if not self.isEnabled():
            skinElement = 'button-disabled'
        elif self.__pressed:
            skinElement = 'button-pressed'
        elif self.isHovered():
            skinElement = 'button-active'
        elif self.isActive():
            skinElement = 'button-active'
        else:
            skinElement = 'button'
        gui.renderElement(surface, self.rect, skinElement)

        self.__textSurface, self.__textRect = getText(self.__text, self.__font, gui.skin[self.skinElement].styles['fontColor'])
        if self.text is not None:
            self.__textRect.x = 2 + self.rect.x + (self.rect.w - self.__textSurface.get_width()) / 2
            self.__textRect.y = 2 + self.rect.y + (self.rect.h - self.__textSurface.get_height()) / 2

        surface.blit(self.__textSurface, self.__textRect)
        # pygame.draw.rect(surface, self.COLOR_INACTIVE, self.rect, 3)

    def onMouseUp(self, event, sender):
        self.__pressed = False
        self.onClick(event, sender)

    def onMouseDown(self, event, sender):
        self.__pressed = True

    def onClick(self, event, sender):
        pass
