import pygame
from core.Character import Character


class NPC(Character):
    attack = 30
    defense = 20
    HP = 500
    xp = 0
    speed = 3
    velocity = [0, 0]
    x = 0
    y = 0
    flag = "NPC"

    def __init__(self, position, reference, name="Henry"):
        super().__init__()
        self.name = name
        self.loadSpriteAnimation(anims.get(self.name))
        self.rect.topleft = position
        self.x = position[0]
        self.y = position[1]
        print(reference)
        self.change_reference_point(reference)
        self.frame = 0

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def collitions(self, objeto):
        pass

    def get_rect(self):
        return pygame.Rect((self.rect.x, self.rect.y + 32, 34, 32))

    def get_flag(self):
        return self.flag
