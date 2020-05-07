import pygame
import os
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
        #self.player = Player((640, 360))
        self.map = Laberinto()

    def render(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.map.handleEvents(event)
            self.map.update()
            #self.player.handle_event(event)
            #if not self.player.act():
                #self.map.changeCoor(self.player.get_x(), self.player.get_y())
            self.screen.fill((0, 0, 0))
            #blits
            self.map.blit(self.screen)
            #self.player.blit(self.screen)
            pygame.display.update()
            self.clock.tick(30)


game = Game()
game.render()
pygame.quit()
