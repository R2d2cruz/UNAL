import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self):
        self.__rect = pygame.Rect((0, 0, 0, 0))
        self.image = None
        self.name = None

    @property
    def x(self):
        return self.__rect.left

    @x.setter
    def x(self, x):
        self.__rect.left = x

    @property
    def y(self):
        return self.__rect.top

    @y.setter
    def y(self, y):
        self.__rect.top = y

    @property
    def width(self):
        return self.__rect.width

    @width.setter
    def width(self, width):
        self.__rect.width = width

    @property
    def height(self):
        return self.__rect.height

    @height.setter
    def height(self, height):
        self.__rect.height = height

    @property
    def rect(self):
        return self.__rect

    def update(self):
        pass

    def render(self, screen, camera):
        screen.blit(self.image, camera.apply(self.__rect))
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.__rect), 1)

    def dispose(self):
        pass

