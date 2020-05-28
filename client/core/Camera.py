import pygame


class Camera:
    def __init__(self, viewWidth, viewHeight, worldWidth, worldHeight):
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        self.target = None
        self.boundLeft = 0
        self.boundRight = -self.worldWidth
        self.boundTop = 0
        self.boundBottom = -self.worldHeight
        self.fixToView = True
        self.view = pygame.Rect(0, 0, viewWidth, viewHeight)
        self.__calculateBounds()

    def __calculateBounds(self):
        if self.fixToView:
            self.boundLeft = -int(self.view.width / 2)
            self.boundRight = -self.worldWidth + int(self.view.width / 2)
            self.boundTop = -int(self.view.height / 2)
            self.boundBottom = -self.worldHeight + int(self.view.height / 2)
        else:
            self.boundLeft = 0
            self.boundRight = -self.worldWidth
            self.boundTop = 0
            self.boundBottom = -self.worldHeight

    def follow(self, target):
        self.target = target

    def apply(self, rect):
        if type(rect) == pygame.Rect:
            return rect.move(self.view.topleft)
        elif type(rect) == tuple:
            return (rect[0] + self.view.x, rect[1] + self.view.y)

    def update(self, deltaTime: float):
        if self.target is not None:
            # calcular  la posicion topLeft de la camara
            self.offsetX = -int(self.target.x + (self.target.width / 2))
            self.offsetY = -int(self.target.y + (self.target.height / 2))

            # limitar el movimiento de la camara para que el foco no se salga del mapa
            self.offsetX = max(self.boundRight, min(self.boundLeft, self.offsetX))
            self.offsetY = max(self.boundBottom, min(self.boundTop, self.offsetY))

            # se mueve la camara a la posicion calculada en el centro de la ventanda
            self.view.x = self.offsetX + int(self.view.width / 2)
            self.view.y = self.offsetY + int(self.view.height / 2)

    def render(self, screen):
        # pintar el view de la camara
        rect = pygame.Rect(
            -self.offsetX - (self.view.width / 2),  # + self.view.x,
            -self.offsetY - (self.view.height / 2),  # + self.view.y,
            self.view.width,
            self.view.height)
        pygame.draw.rect(screen, (255, 0, 0), self.apply(rect), 1)
        rect = pygame.Rect(
            0,
            0,
            self.worldWidth,
            self.worldHeight)
        pygame.draw.rect(screen, (0, 255, 0), self.apply(rect), 1)
