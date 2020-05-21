import pygame
import os
if os.name != "nt":
    from constants import imgsOS as imgs, animsOS as anims, fontsOS as fonts
    from core.Character import Character
else:
    from client.constants import imgsNT as imgs, animsNT as anims, fontsNT as fonts
    from client.core.Character import Character


class OnlinePlayer(Character):
    def __init__(self, information, *groups):
        super().__init__(*groups)
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
        self.x = information.get("x")
        self.y = information.get("y")
        self.nameTack = information.get("n")
        font = pygame.font.Font(fonts.get("minecraft"), 14)
        self.textNameTack = font.render(self.nameTack, 0, (0, 0, 0))
        self.name = "Henry"
        self.loadAnimation(anims.get(self.name))
        self.movement = self.traductor.get(information.get("a"))
        self.rect = pygame.Rect(0, 0, 34, 32)
        self.rect.topleft = (self.x, self.y)

    def setPos(self, information, *args):
        self.x = information.get("x")
        self.y = information.get("y")
        self.action = self.traductor.get(information.get("a"))

    def update(self, *args):
        if self.action is not None:
            super().update(self.action)

    def render(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.textNameTack, (self.rect.topleft[0] + (34 - self.textNameTack.get_width()) / 2,
                                        self.rect.topleft[1] - 14))

