import pygame
import json


class Character(pygame.sprite.Sprite):
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
        self.image = 0
        self.rect = None
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

    def loadImg(self, fileName):
        self.sheet = pygame.image.load(fileName)
        self.sheet.set_clip(pygame.Rect(37, 1, 34, 56))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = pygame.Rect(37, 1, 34, 32)  # self.image.get_rect()

    def blit(self, screen):
        # pygame.draw.rect(screen, (0, 255, 0), self.get_rect())
        screen.blit(self.image, self.rect)

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

    def get_velocity(self):
        return self.velocity

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]
