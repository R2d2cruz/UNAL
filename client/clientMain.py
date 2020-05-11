import pygame
import os
import zmq
from client.laberinto import Laberinto

print(os.getcwd())
directory = str(os.getcwd())
pygame.init()


class Game:
    screen = pygame.display.set_mode((1280, 720))
    run = True
    pygame.display.set_icon(pygame.image.load("unallogo.jpg"))
    clock = pygame.time.Clock()

    def __init__(self):
        context = zmq.Context()
        print("Connecting to hello world server…")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self.socket.send_string("createPlayer")
        self.id = self.socket.recv_string()
        print(self.id)

        self.map = Laberinto(self)

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


game = Game()
game.render()
pygame.quit()