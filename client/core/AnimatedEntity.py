import pygame
import json
import os


class AnimatedEntity(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.frame = 0
        self.sheet = None
        self.image = None
        self.rect = pygame.Rect((0, 0, 0, 0))

    def loadAnimation(self, fileName):
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

    def render(self, screen):
        screen.blit(self.image, self.rect)