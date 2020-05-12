import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.rect = pygame.Rect((0, 0, 0, 0))

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def dispose(self):
        pass

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]

    def render(self, screen):
        screen.blit(self.image, self.rect)
        
    def get_rect(self):
        return self.rect

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
