import pygame
from core.Scene import Scene
from core.Map import Map
from core.Game import Game


class Playground(Scene):
    def __init__(self, game: Game, map: Map):
        super().__init__(game)
        self.map = map

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.setScene("main")
            else:
                self.map.player.move(self.KEYDOWN.get(event.key))
        elif event.type == pygame.KEYUP:
            self.map.player.move((self.KEYUP.get(event.key)))

    def update(self):
        self.map.update()

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.map.blit(screen)
