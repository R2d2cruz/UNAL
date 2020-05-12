import pygame
import json
import os

if os.name == "nt":
    # noinspection PyUnresolvedReferences
    from core.AnimatedEntity import AnimatedEntity
else:
    from client.core.AnimatedEntity import AnimatedEntity


class Character(AnimatedEntity):

    def __init__(self, *groups):
        super().__init__(*groups)
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

    def to_json(self):
        return json.dumps({
            "x": self.rect.topleft[0] - self.x,
            "y": self.rect.topleft[1] - self.y,
            "a": self.traductor.get(self.action)
        })

    def get_velocity(self):
        return self.velocity
