import zmq
import pygame
import os
import sys

if os.name == 'nt':
    from client.constants import imgs
    from client.laberinto import Laberinto
    from client.config import Config
else:
    from constants import imgs
    from Laberinto import Laberinto
    from Config import Config

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

    run = True
    updateables = []
    drawables = []

    def __init__(self):
        self.id = None
        self.connected = False
        self.socket = None
        self.connect()
        pygame.init()
        pygame.display.set_icon(pygame.image.load(imgs.get("logo")))
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.map = Laberinto(self)

    def connect(self):
        config = Config()
        context = zmq.Context()
        maxAttempts = config.maxAttemptsPerServer
        attempt = 0
        for server in config.servers:
            for i in range(1, maxAttempts + 1):
              try:
                  print("Conectandose a servidor " + server + " (intento " +  str(i) + ")")
                  self.socket = context.socket(zmq.REQ)
                  self.socket.setsockopt(zmq.SNDTIMEO, 1000)
                  self.socket.setsockopt(zmq.RCVTIMEO, 1000)
                  self.socket.setsockopt(zmq.LINGER, 1000)
                  self.socket.connect("tcp://" + server)
                  self.connected = True
                  self.socket.send_string("createPlayer")
                  self.id = self.socket.recv_string()
                  print("Conexión exitosa. Id de cliente: " + self.id)
                  return
              except Exception as e:
                  print(e)
                  self.socket.close()

        print("No se pudo conectar. Por favor verifique que la configuración en config.json sea correcta y vuelva a intentar.")
        context.term()
        pygame.quit()
        sys.exit()

    def get_id(self):
        return self.id

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if self.map.player:
                if event.type == pygame.KEYDOWN:
                    self.map.player.update(self.KEYDOWN.get(event.key))

                if event.type == pygame.KEYUP:
                    self.map.player.velocity = [0, 0]
                    self.map.player.update((self.KEYUP.get(event.key)))

    def update(self):
        self.map.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        #blits
        self.map.blit(self.screen)
        pygame.display.update()
        self.clock.tick(30)

    def run(self):
        while self.run:
            self.handleEvents()
            self.update()
            self.render()
