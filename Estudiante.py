import pygame
import os

found = os.getcwd()

class Estudiante(pygame.sprite.Sprite):

    def __init__(self, position, name="Henry", *groups):
        super().__init__(*groups)
        self.name = name
        self.sheet = pygame.image.load(found + "\\Assets\\" + self.name + ".png")
        self.sheet.set_clip(pygame.Rect(64, 0, 34, 56))
        self.image = self.sheet.surface(self.sheet.get_clip())
        self.rect = self.sheet.get_Rect
        self.rect.topleft = position
        self.frame = 0
        self.front = {0: (37, 1, 34, 56)}
        self.back = {0: (1, 1, 34, 56)}
        self.left = {0: (217, 1, 32, 56)}
        self.right = {0: (251, 1, 32, 56)}
        self.walk = {0: (357, 1, 34, 53), 1: (393, 1, 34, 53)}
        self.backWalk = {0: (285, 1, 34, 54), 1: (321, 1, 34, 54)}
        self.leftWalk = {0: (109, 1, 34, 56), 1: (181, 1, 34, 56)}
        self.rightWalk = {0: (73, 1, 34, 56), 1: (145, 1, 34, 56)}

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(clipped_rect)
        return clipped_rect


    def update(self, direction):
        if direction == "up":
            self.clip(self.backWalk)
        if direction == "down":
            self.clip(self.walk)
        if direction == "right":
            self.clip(self.rightWalk)

