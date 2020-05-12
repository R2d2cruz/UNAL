import pygame
import json
import os

from core.Entity import Entity


class AnimatedEntity(Entity):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.frame = 0
        self.sheet = None
        self.currentClip = None
        self.lastFrameTime = 0
        self.timeStep = 50

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
        self.currentClip = data.get("default_sprite")
        self.clip(self.currentClip)

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipName):
        clipFrame = self.clips.get(clipName)
        frameRect = self.get_frame(clipFrame)
        self.sheet.set_clip(pygame.Rect(frameRect))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect.w = frameRect[2]
        self.rect.h = frameRect[3]

    def update(self):
        t = pygame.time.get_ticks()
        deltaTime = (t - self.lastFrameTime)
        if deltaTime >= self.timeStep:
          self.lastFrameTime = t
          self.clip(self.currentClip)