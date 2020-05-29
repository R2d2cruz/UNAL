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
        self.width = data.get("width")
        self.height = data.get("height")
        self.timeStep = data.get("timestep")
        self.currentClip = data.get("default_sprite")
        self.getNextFrame()

    def getFrame(self, frameSet):
        self.frame += 1
        if self.frame > (len(frameSet) - 1):
            self.frame = 0
        return frameSet[self.frame]

    def getNextFrame(self):
        clipFrame = self.clips.get(self.currentClip)
        frameRect = self.getFrame(clipFrame)
        self.sheet.set_clip(pygame.Rect(frameRect))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.width = frameRect[2]
        self.height = frameRect[3]

    def update(self, deltaTime: float):
        # ojo, esto se totea cuando al character no se le setea animacion
        self.lastFrameTime += deltaTime
        if self.lastFrameTime >= self.timeStep:
            self.lastFrameTime -= self.timeStep
            self.getNextFrame()


# class Animation:
#     frames = []
#     lapse = 0
#     N = 0
#     loop = False
#     time = 0

#     def __init__(self, frames, lapse=1, loop=False):
#         self.frames = frames
#         self.lapse = lapse
#         self.N = len(frames)
#         self.loop = loop

#     def update(self, deltaTime: float):
#         self.time += deltaTime

#     def reset(self):
#         self.time = 0

#     def getFrame(self, loop):
#         n = int(self.time / self.lapse)
#         if loop and n > self.N:
#             n = n % self.N
#         return self.frames[n - 1]
