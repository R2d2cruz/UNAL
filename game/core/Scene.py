import pygame

LEFT = 1
RIGHT = 3


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
        self.ui = None
        self.game = game

    def init(self):
        pass

    def onEnterScene(self, data: dict = None):
        pass

    def onExitScene(self):
        pass

    def handleKeyEvent(self, event) -> bool:
        if self.ui.handleKeyEvent(event):
            return True
        if event.type == pygame.KEYDOWN:
            self.onKeyDown(event)
        elif event.type == pygame.KEYUP:
            self.onKeyUp(event)
        return True

    def handleMouseEvent(self, event) -> bool:
        if self.ui.handleMouseEvent(event):
            return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == RIGHT:
                self.onRightMouseDown(event)
            else:
                self.onLeftMouseDown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == RIGHT:
                self.onRightMouseUp(event)
            else:
                self.onLeftMouseUp(event)
        elif event.type == pygame.MOUSEMOTION:
            self.onMouseMove(event)
        return True

    def onKeyDown(self, event):
        pass

    def onKeyUp(self, event):
        pass

    def onRightMouseDown(self, event):
        pass

    def onRightMouseUp(self, event):
        pass

    def onLeftMouseDown(self, event):
        pass

    def onLeftMouseUp(self, event):
        pass

    def onMouseMove(self, event):
        pass

    def update(self, deltaTime: float):
        pass

    def render(self, surface):
        pass
