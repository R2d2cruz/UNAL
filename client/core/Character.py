import pygame
import json
import os

from core.AnimatedEntity import AnimatedEntity

class Character(AnimatedEntity):
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

    def __init__(self, *groups):
        super().__init__(*groups)
        self.frame = 0
        self.sheet = None
        self.velocity = [0, 0]
        self.x = 0
        self.y = 0
        self.action = None

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def to_json(self):
        return json.dumps({
            "x": self.rect.topleft[0] - self.x,
            "y": self.rect.topleft[1] - self.y,
            "a": self.traductor.get(self.action)
        })

    def get_velocity(self):
        return self.velocity

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]
