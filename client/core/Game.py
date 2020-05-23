import pygame
import sys
import os

if os.name != "nt":
    from core.Config import Config
    from core.Client import Client
    from core.Scene import Scene
    from core.Map import Map
    from core.ResourceHandler import ResourceHandler
else:
    from client.core.Config import Config
    from client.core.Client import Client
    from client.core.Scene import Scene
    from client.core.Map import Map
    from client.core.ResourceHandler import ResourceHandler


class Game:
    def __init__(self, res: ResourceHandler, config: Config):
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
                self.isRunning = False
                continue
            self.currentScene.handleEvent(event)

    def update(self):
        self.currentScene.update()

    def render(self):
        self.currentScene.render(self.screen)
        pygame.display.update()
        self.clock.tick(30)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handleEvents()
            self.update()
            self.render()

    def quit(self):
        self.isRunning = False
        self.client.close()
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
