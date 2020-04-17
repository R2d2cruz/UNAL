import pygame


class Objects:

    rect = pygame.Rect((0, 0, 32, 32))
    frames = [

    ]
    i = 0
    flag = "object"

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.rect.topleft = [x, y]
        self.x = x
        self.y = y

    def blit(self, screen):
        screen.blit(self.frames[self.i], self.rect)

    def get_rect(self):
        return self.rect

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]


class Rock(Objects):

    def __init__(self, x, y):
        super().__init__(x, y)
        image = pygame.image.load("RPG Nature Tileset.png")
        self.frames = {
            0: image.subsurface((64, 32, 32, 32))
        }

