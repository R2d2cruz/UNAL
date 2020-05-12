import pygame
import sys

from constants import imgs
from Laberinto import Laberinto
from core.Client import Client

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
        self.client = Client()
        if self.client.connect(config):
            self.init()
        else:
            pygame.quit()
            sys.exit()

    def init(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load(imgs.get("logo")))
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.map = Laberinto(self)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            #if self.map.player:
            if event.type == pygame.KEYDOWN:
                self.map.player.move(self.KEYDOWN.get(event.key))

            if event.type == pygame.KEYUP:
                self.map.player.move((self.KEYUP.get(event.key)))

    def update(self):
        self.map.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        #blits
        self.map.blit(self.screen)
        pygame.display.update()
        self.clock.tick(30)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.handleEvents()
            self.update()
            self.render()
