import pygame

from .Control import Control
from .gui import gui
from ..core.camera import BaseCamera
from ..core.misc import getText


class Button(Control):

    skinElement = 'button'

    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font = None, text: str = '',
                 foreColor=Control.WHITE):
        super().__init__(x, y, width, height)
        self.__textSurface = None
        self.__textRect = pygame.Rect(0, 0, 0, 0)
        self.__font = font
        self.__color = foreColor
        self.__pressed = False
        self.__skinState = 'default'
        self.__image = None
        self.text = text
        self.backColor = (123, 123, 123)

    def __refreshText(self):
        if self.__text is not None and self.__font is not None:
            self.__textSurface, self.__textRect = getText(
                self.__text, self.__font,
                gui.skin[Button.skinElement].styles['fontColor']
            )
            if self.text is not None:
                self.__textRect.x = 2 + self.rect.x + (self.rect.w - self.__textSurface.get_width()) / 2
                self.__textRect.y = 2 + self.rect.y + (self.rect.h - self.__textSurface.get_height()) / 2

    def refresh(self):
        self.__refreshText()
        imgWidth = self.__textRect.w if self.image is None else self.image.get_width()
        imgHeight = self.__textRect.h if self.image is None else self.image.get_height()
        self.rect.width = max(self.width, gui.skin[Button.skinElement].getMinWidth() + imgWidth)
        self.rect.height = max(self.height, gui.skin[Button.skinElement].getMinHeight() + imgHeight)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.refresh()

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image
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
            self.__skinState = 'disabled'
        elif self.__pressed:
            self.__skinState = 'pressed'
        elif self.isHovered():
            self.__skinState = 'active'
        elif self.isActive():
            self.__skinState = 'active'
        else:
            self.__skinState = 'default'
        gui.renderElement(surface, self.rect, Button.skinElement, self.__skinState)

        if self.image is not None:
            rect = self.image.get_rect()
            rect.center = self.rect.center
            surface.blit(self.image, rect)

        self.__refreshText()
        if self.__textSurface is not None:
            surface.blit(self.__textSurface, self.__textRect)
            # pygame.draw.rect(surface, self.COLOR_INACTIVE, self.rect, 3)

    def onMouseUp(self, event, sender):
        self.__pressed = False
        self.onClick(event, sender)

    def onMouseDown(self, event, sender):
        self.__pressed = True

    def onClick(self, event, sender):
        pass
