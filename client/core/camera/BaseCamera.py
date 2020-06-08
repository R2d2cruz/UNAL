import pygame

class BaseCamera:
    def __init__(self, viewWidth, viewHeight, worldWidth, worldHeight):
        pass

    def follow(self, target):
        pass

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return rect

    def update(self, deltaTime: float):
        pass

    def render(self, screen):
        pass