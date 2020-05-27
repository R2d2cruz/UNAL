import pygame
import sys
from core.Config import Config
from core.Client import Client
from core.Scene import Scene
from core.ResourceManager import ResourceManager


class Game:
    def __init__(self, res: ResourceManager, config: Config):
        self.scenes = {}
        self.res = res
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
        pygame.display.set_icon(self.res.loadImage("logo"))
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.mixer = pygame.mixer.music
        self.mixer.set_volume(self.config.volume)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                continue
            self.currentScene.handleEvent(event)
        if not self.client.connected:
            self.currentScene.handleMessage('diconnected')

    def update(self):
        self.currentScene.update()

    def render(self):
        self.currentScene.render(self.screen)
        pygame.display.update()
        self.clock.tick(200)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handleEvents()
            self.update()
            self.render()

    def quit(self):
        self.client.disconnect()
        self.isRunning = False
        pygame.quit()
        sys.exit()

    def setScene(self, name: str):
        if self.currentScene is not None:
            self.currentScene.onExit()
        self.currentScene = self.scenes.get(name)
        if self.currentScene is not None:
            self.currentScene.onEnter()

    def addScene(self, name: str, scene: Scene):
        self.scenes[name] = scene

    def setPlayer(self, player):
        self.player = player

    def playSound(self, name):
        try:
            self.mixer.load(self.res.getSoundPath(name))
            self.mixer.play(-1)
        except Exception as e:
            print("😞 No se pudo cargar audio " +
                  self.res.getSoundPath(name), e)
