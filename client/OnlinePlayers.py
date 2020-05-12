import pygame
import os
if os.name != "nt":
    from constants import imgsOS as imgs
    from core.Character import Character
else:
    from client.constants import imgsNT as imgs
    from client.core.Character import Character


class OnlinePlayer(Character):
    def __init__(self, information, *groups):
        super().__init__(*groups)
        self.x = information.get("x") - 12
        self.y = information.get("y") - 4
        self.name = "Diego"      
        self.image = pygame.image.load(imgs.get(self.name))
        self.movement = information.get("a")
        self.rect = pygame.Rect(37, 1, 34, 32)
        self.rect.topleft = (self.x, self.y)
