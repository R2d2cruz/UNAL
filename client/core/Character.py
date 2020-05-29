import json
import pygame
import core.ResourceManager as res
from core.MovingEntity import MovingEntity


compassClips = ['right', 'down', 'down', 'down', 'left', 'up', 'up', 'up']
traductor = {
    "stand_up": "stu",
    "stand_down": "std",
    "stand_left": "stl",
    "stand_right": "str",
    "up": "wlu",
    "down": "wld",
    "left": "wll",
    "right": "wlr"
}


class Character(MovingEntity):
    def __init__(self, name: str, animationName: str, position, *groups):
        super().__init__(position, *groups)
        self.__color = (0, 0, 0)
        self.__nameSurface = None
        self.__nameRect = None
        self.setName(name)
        self.animName = animationName
        self.loadAnimation(res.getAnimFile(self.animName))

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.__nameRect.x, self.__nameRect.y = (
            self.x + (34 - self.__nameRect.width) / 2, self.y - 14)
        direction = compassClips[self.heading.getCompass()]
        self.currentClip = (
            'stand_' if self.velocity.isZero() else '') + direction

    def render(self, screen, camera):
        super().render(screen, camera)
        if self.name is not None:
            if self.__nameSurface is not None:
                screen.blit(self.__nameSurface, camera.apply(self.__nameRect))

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=traductor.get(self.currentClip)
        )

    def setName(self, name: str):
        if name is not None or name != '':
            self.name = name
            font = res.getFont('minecraft', 14)
            self.__nameSurface, self.__nameRect = res.getText(
                self.name, font, self.__color)
        else:
            self.__nameSurface = None
            self.__nameRect = None
            self.name = None

    def collitions(self, rect: pygame.Rect):
        pass
