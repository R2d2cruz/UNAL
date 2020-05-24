import json
import pygame
from core.AnimatedEntity import AnimatedEntity


class Character(AnimatedEntity):
    def __init__(self, game, *groups):
        super().__init__(*groups)
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
        self.velocity = [0, 0]
        self.action = None
        self.textNameTack = None
        self.nameRect = pygame.Rect(0, 0, 0, 0)

    def update(self, action):
        super().update(action)
        self.nameRect.x = self.x + (34 - self.textNameTack.get_width()) / 2
        self.nameRect.y = self.y - 14

    def render(self, screen, camera):
        super().render(screen, camera)
        if self.name is not None:
            if self.textNameTack is not None:
                screen.blit(self.textNameTack, camera.apply(self.nameRect))

    def toDict(self):
        return dict(
            x = self.x,
            y = self.y,
            a = self.traductor.get(self.action)
        )

    def get_velocity(self):
        return self.velocity

    def set_name(self, name: str):
        if name is not None or name != '':
            self.name = name
            font = self.game.res.getFont('minecraft', 14)
            self.textNameTack = font.render(self.name, 0, (0, 0, 0))
        else:
            self.name = None
            self.nameRect = None
