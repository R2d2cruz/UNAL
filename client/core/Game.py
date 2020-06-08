import pygame
import sys
import json
import core.Hermes as Hermes
import core.ResourceManager as res
from core.Config import Config
from core.Client import Client
from core.Scene import Scene
from core.Message import Message


class Game:
    def __init__(self, config: Config):
        self.scenes = {}
        self.config: Config = config
        self.isRunning = False
        self.screen = None
        self.clock = None
        self.currentScene = None
        self.player = None
        self.client = Client(self.config)
        pygame.init()
        pygame.mixer.init()

    def init(self):
        pygame.display.set_icon(res.loadImage("logo"))
        self.screen = pygame.display.set_mode((self.config.windowWidth, self.config.windowHeight))
        self.clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(self.config.volume)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                continue
            self.currentScene.handleEvent(event)
        if not self.client.connected:
            self.currentScene.handleMessage(Message(Message.DISCONNECTED))

    def update(self, deltaTime: float):
        self.currentScene.update(deltaTime)

    def render(self):
        self.currentScene.render(self.screen)
        pygame.display.update()
        self.clock.tick(200)

    def run(self):
        self.isRunning = True
        lastFrameTime = 0
        while self.isRunning:
            self.handleEvents()
            t = pygame.time.get_ticks()
            self.update((t - lastFrameTime))
            lastFrameTime = t
            Hermes.setDeltaTime(t)
            self.render()

    def quit(self):
        self.client.disconnect()
        self.isRunning = False
        pygame.quit()
        sys.exit()

    def setScene(self, name: str):
        if self.currentScene is not None:
            self.currentScene.onExitScene()
        self.currentScene = self.scenes.get(name)
        if self.currentScene is not None:
            self.currentScene.onEnterScene()

    def addScene(self, name: str, scene: Scene):
        self.scenes[name] = scene

    def setPlayer(self, player):
        self.player = player

    def loadSettings(self):
        try:
            with open('saves/player.save', 'r') as infile:
                data = json.load(infile)
                self.player.name = data.get('name')
        except Exception:
            pass

    def saveSettings(self):
        with open('saves/player.save', 'w') as outfile:
            json.dump(dict(name=self.player.name), outfile)
