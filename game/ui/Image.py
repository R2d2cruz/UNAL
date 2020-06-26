import pygame

from .Control import Control
from ..core.camera import BaseCamera
from ..core.misc import Colors


class Image(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.__surface = None

    def refresh(self):
        if self.__surface is not None:
            self.rect.width = self.__surface.get_width()
            self.rect.height = self.__surface.get_height()

    @property
    def image(self):
        return self.__surface

    @image.setter
    def image(self, image):
        self.__surface = image
        self.refresh()

    def onRender(self, surface, camera: BaseCamera):
        surface.blit(self.__surface, self.rect)
        pygame.draw.rect(surface, Colors.GRAY, self.rect, 3)

    def onMouseUp(self, event):
        self.onClick(self)

    def onClick(self, sender):
        pass
