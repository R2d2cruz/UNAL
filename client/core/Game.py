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
        pygame.init()
        pygame.mixer.init()

    def init(self):
        pygame.display.set_icon(self.res.loadImage("logo"))
        self.mixer = pygame.mixer.music
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.playSound()

    def connectClient(self):
        self.client = Client(self.config, self.player.name)
        if not self.client.connect():
            self.client.close()
            pygame.quit()
            sys.exit()

    def playSound(self):
        try:
            self.mixer.load(self.res.getSoundPath("music"))
            self.mixer.set_volume(self.config.volume)
            self.mixer.play()
        except:
            print("😞 No se pudo cargar audio")

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                continue
            self.currentScene.handleEvent(event)

    def update(self):
        self.currentScene.update()

    def render(self):
        # self.screen.fill((0, 0, 0))
        self.currentScene.render(self.screen)
        pygame.display.update()
        # pygame.display.flip()  ??????
        self.clock.tick(30)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handleEvents()
            self.currentScene.update()
            self.render()

    def setScene(self, name: str):
        self.currentScene = self.scenes.get(name)

    def addScene(self, name: str, scene: Scene):
        self.scenes[name] = scene

    def setPlayer(self, player):
        self.player = player