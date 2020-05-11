import pygame


class OnlinePlayer(pygame.sprite.Sprite):

    image = pygame.image.load("Diego.png")

    def __init__(self, information, *groups):
        super().__init__(*groups)
        self.x = information.get("x") - 12
        self.y = information.get("y") - 4
        self.movement = information.get("a")
        self.rect = pygame.Rect(37, 1, 34, 32)
        self.rect.topleft = (self.x, self.y)

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]
