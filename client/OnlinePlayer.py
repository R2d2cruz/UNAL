import pygame
import core.ResourceManager as res
from core.Character import Character


class OnlinePlayer(Character):
    def __init__(self, game, data, *groups):
        super().__init__(game, *groups)
        self.traductor = {
            "stu": "stand_up",
            "std": "stand_down",
            "stl": "stand_left",
            "str": "stand_right",
            "wlu": "up",
            "wld": "down",
            "wll": "left",
            "wlr": "right"
        }
        self.set_name(data.get("n"))
        self.loadAnimation(res.getRandomCharAnimFile())
        self.movement = self.traductor.get(data.get("a"))
        self.x = data.get("x")
        self.y = data.get("y")
        self.width = 34
        self.height = 32
        self.rect.topleft = (self.x, self.y)

    def setPos(self, data):
        self.x = data.get("x")
        self.y = data.get("y")
        self.currentClip = self.traductor.get(data.get("a"))
