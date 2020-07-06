import pygame

from .Control import Control
from ..core.camera import BaseCamera


class AnimatedBox(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.__anim = None

    @property
    def animation(self):
        return self.__anim

    @animation.setter
    def animation(self, anim):
        self.__anim = anim
        self.refresh()

    def refresh(self):
        self.__anim.center = self.rect.center

    def update(self, deltaTime: float):
        if self.__anim is not None:
            self.__anim.uppdate(deltaTime)

    def onRender(self, surface, camera: BaseCamera):
        if self.__anim is not None:
            self.__anim.render(surface, camera)

        pygame.draw.rect(surface, (0,0,0), camera.apply(self.rect), 1)

    def onMouseUp(self, event, sender):
        self.onClick(event, sender)

    def onClick(self, event, sender):
        pass
