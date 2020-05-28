import pygame


class Scene:
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

    def __init__(self, game):
        self.game = game

    def init(self):
        pass

    def onEnterScene(self):
        pass

    def onExitScene(self):
        pass

    def handleEvent(self, event):
        pass

    def handleMessage(self, message):
        pass

    def update(self, deltaTime: float):
        pass

    def render(self, screen):
        pass
