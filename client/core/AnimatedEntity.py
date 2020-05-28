import pygame
import json
import core.ResourceManager as res
from core.Entity import Entity


class AnimatedEntity(Entity):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.frame = 0
        self.sheet = None
        self.image = None
        self.currentClip = None
        self.lastFrameTime = 0
        self.timeStep = 100
        self.clips = {}
        self.width = 0
        self.height = 0

    def handleEvent(self, event):
        pass

    def loadAnimation(self, fileName: str):
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
        self.width = frameRect[2]
        self.height = frameRect[3]

    def update(self, deltaTime: float):
        # ojo, esto se totea cuando al character no se le setea animacion
        self.lastFrameTime += deltaTime
        if self.lastFrameTime >= self.timeStep:
            self.lastFrameTime -= self.timeStep
            self.clip(self.currentClip)
            
