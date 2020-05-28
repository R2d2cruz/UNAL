import json
import pygame
import core.ResourceManager as res
from core.MovingEntity import MovingEntity


class Character(MovingEntity):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.__nameSurface = None
        self.name = None
        self.game = game
        self.traductor = {
            "stand_up": "stu",
            "stand_down": "std",
            "stand_left": "stl",
            "stand_right": "str",
            "up": "wlu",
            "down": "wld",
            "left": "wll",
            "right": "wlr"
        }
        self.action = None
        self.__color = (0, 0, 0)
        self.__nameRect = pygame.Rect(0, 0, 0, 0)

    def update(self):
        super().update()
        self.__nameRect.x, self.__nameRect.y = (self.x + (34 - self.__nameRect.width) / 2, self.y - 14)

    def render(self, screen, camera):
        super().render(screen, camera)
        if self.name is not None:
            if self.__nameSurface is not None:
                screen.blit(self.__nameSurface, camera.apply(self.__nameRect))

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=self.traductor.get(self.action)
        )

    def set_name(self, name: str):
        if name is not None or name != '':
            self.name = name
            font = res.getFont('minecraft', 14)
            self.__nameSurface, self.__nameRect = res.getText(self.name, font, self.__color)
        else:
            self.__nameSurface = None
            self.__nameRect = None
            self.name = None
