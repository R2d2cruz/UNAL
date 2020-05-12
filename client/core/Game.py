import pygame
import sys
import os
import json

if os.name != "nt":
    from constants import imgsOS as imgs, soundsOS as sounds
    from Laberinto import Laberinto
    from core.Client import Client
else:
    from client.constants import imgsNT as imgs, soundsNT as sounds
    from client.Laberinto import Laberinto
    from client.core.Client import Client


class Game:
    KEYDOWN = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right"
    }

    KEYUP = {
        pygame.K_UP: "stand_up",
        pygame.K_DOWN: "stand_down",
        pygame.K_LEFT: "stand_left",
        pygame.K_RIGHT: "stand_right"
    }

    def __init__(self, config):
        self.isRunning = False
        self.screen = None
        self.clock = None
        self.map = None
        self.mixer = pygame.mixer.music
        with open(sounds.get("sounds")) as json_file:
            self.music = json.load(json_file)
        self.client = Client(config)
        if self.client.connect():
            self.init()
        else:
            self.client.close()
            pygame.quit()
            sys.exit()

    def init(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load(imgs.get("logo")))
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.mixer.load(("../" if os.name == "nt" else "") + self.music.get("music"))
        self.mixer.set_volume(sounds.get("volume"))
        self.mixer.play()
        self.map = Laberinto(self)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.KEYDOWN:
                self.map.player.move(self.KEYDOWN.get(event.key))

            if event.type == pygame.KEYUP:
                self.map.player.move((self.KEYUP.get(event.key)))

    def update(self):
        self.map.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map.blit(self.screen)
        pygame.display.update()
        self.clock.tick(30)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handleEvents()
            self.update()
            self.render()
