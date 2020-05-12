import pygame
import json
import os


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
        self.rect = pygame.Rect((0, 0, 0, 0))
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

    def loadSpriteAnimation(self, fileName):
        self.clips = {}
        with open(fileName) as json_file:
            data = json.load(json_file)
            if os.name != "nt":
                imgFile = data.get("image")
            else:
                imgFile = "../" + data.get("image")
            self.sheet = pygame.image.load(imgFile)
            sprites = data.get("sprites")
            for key in sprites:
                self.clips[key] = sprites[key]
        self.clip("stand_down")

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipName):
        clipFrame = self.clips.get(clipName)
        frame = self.get_frame(clipFrame)
        self.sheet.set_clip(pygame.Rect(frame))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect.w = frame[2]
        self.rect.h = frame[3]

    def get_velocity(self):
        return self.velocity

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]
