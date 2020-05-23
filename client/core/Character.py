import pygame
import json
import os

if os.name != "nt":
    from core.AnimatedEntity import AnimatedEntity
else:
    from client.core.AnimatedEntity import AnimatedEntity


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
        self.frame = 0
        self.sheet = None
        self.velocity = [0, 0]
        self.x = 0
        self.y = 0
        self.action = None
        self.textNameTack = None
        self.nameRect = None

    def render(self, screen):
        screen.blit(self.image, self.rect)
        if self.textNameTack is not None:
            self.nameRect = (
                self.rect.topleft[0] + (34 - self.textNameTack.get_width()) / 2,  self.rect.topleft[1] - 14)
            screen.blit(self.textNameTack, self.nameRect)

    def to_json(self):
        return json.dumps({
            "x": self.rect.topleft[0] - self.x,
            "y": self.rect.topleft[1] - self.y,
            "a": self.traductor.get(self.action)
        })

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
