import pygame
from constants import imgs
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

    def __init__(self, position, reference, name="Henry", *groups):
        super().__init__(*groups)
        self.name = name
        self.loadImg()
        self.x = position[0]
        self.y = position[1]
        print(reference)
        self.change_reference_point(reference)
        self.frame = 0
        self.front = {0: (37, 1, 34, 56)}
        self.back = {0: (1, 1, 34, 56)}
        self.left = {0: (217, 1, 32, 56)}
        self.right = {0: (251, 1, 32, 56)}

    def loadImg(self):
        self.sheet = pygame.image.load(imgs.get(self.name)
        self.sheet.set_clip(pygame.Rect(37, 1, 34, 56))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = pygame.Rect(37, 1, 34, 32)  # self.image.get_rect()

    def act(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def get_x(self):
        return self.rect.topleft[0]

    def get_y(self):
        return self.rect.topleft[1]

    def collitions(self, objeto):
        pass

    def get_rect(self):
        return pygame.Rect((self.rect.x, self.rect.y + 32, 34, 32))

    def get_flag(self):
        return self.flag
