import sys

import pygame

from .Client import Client
from .Config import Config
from .Hermes import hermes
from .ResourceManager import resourceManager
from .Scene import Scene

mouseEvents = [
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONUP
]
keyEvents = [
    pygame.KEYUP,
    pygame.KEYDOWN
]


class Game:
    def __init__(self, config: Config):
        self.scenes = {}
        self.config: Config = config
        self.isRunning = False
        self.surface = None
        self.windowWidth = self.config.windowWidth
        self.windowHeight = self.config.windowHeight
        self.clock = None
        self.currentScene = None
        self.client = Client(self.config)
        pygame.init()
        pygame.mixer.init()

    def init(self):
        pygame.display.set_icon(resourceManager.loadImage("logo"))
        self.surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(self.config.volume)

    def handleEvents(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWEVENT:
                self.quit()
                return True
            elif event.type in mouseEvents:
                if self.currentScene.handleMouseEvent(event):
                    return True
            elif event.type in keyEvents:
                if self.currentScene.handleKeyEvent(event):
                    return True
        return False

    def update(self, deltaTime: float):
        self.currentScene.update(deltaTime)

    def render(self):
        self.currentScene.render(self.surface)
        pygame.display.update()
        self.clock.tick(20)

    def run(self):
        self.isRunning = True
        lastFrameTime = 0
        while self.isRunning:
            self.handleEvents()
            t = pygame.time.get_ticks()
            self.update((t - lastFrameTime))
            lastFrameTime = t
            hermes.setDeltaTime(t)
            self.render()

    def quit(self):
        self.client.disconnect()
        self.isRunning = False
        pygame.quit()
        sys.exit()

    def setScene(self, name: str, data: dict = None):
        if self.currentScene is not None:
            self.currentScene.onExitScene()
        self.currentScene = self.scenes.get(name)
        if self.currentScene is not None:
            self.currentScene.onEnterScene(data)

    def addScene(self, name: str, scene: Scene):
        self.scenes[name] = scene
