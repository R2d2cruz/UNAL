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
    from laberinto import Laberinto
    from Config import Config

class Game:
    run = True

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

    def render(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.map.handleEvents(event)
            self.map.update()
            self.screen.fill((0, 0, 0))
            #blits
            self.map.blit(self.screen)
            pygame.display.update()
            self.clock.tick(30)