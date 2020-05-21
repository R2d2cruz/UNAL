import pygame
import json
import os

if os.name != "nt":
    from core.Entity import Entity
else:
    from client.core.Entity import Entity


class AnimatedEntity(Entity):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.frame = 0
        self.sheet = None
        self.currentClip = None
        self.lastFrameTime = 0
        self.timeStep = 50
        self.clips = {}

    def loadAnimation(self, fileName: str, res):
        with open(fileName) as json_file:
            data = json.load(json_file)
            self.sheet = res.loadImageByPath(res.fixPath(data.get("image")))
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

    def clip(self, clipName: str):
        clipFrame = self.clips.get(clipName)
        frameRect = self.get_frame(clipFrame)
        self.sheet.set_clip(pygame.Rect(frameRect))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect.w = frameRect[2]
        self.rect.h = frameRect[3]

    def update(self, clip=None):
        t = pygame.time.get_ticks()
        deltaTime = (t - self.lastFrameTime)
        if deltaTime >= self.timeStep:
            self.lastFrameTime = t
            if clip is None:
                self.clip(self.currentClip)
            else:
                self.clip(clip)
