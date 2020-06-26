import pygame

from .Control import Control
from .gui import gui
from ..core.camera import BaseCamera
from ..core.misc import getText


class Image(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.__surface = None

    @property
    def image(self):
        return self.__surface

    @image.setter
    def image(self, image):
        self.__surface = image

    def onRender(self, surface, camera: BaseCamera):
        surface.blit(self.__surface, self.rect)

    def onMouseUp(self, event):
        self.onClick(self)

    def onClick(self, sender):
        pass
