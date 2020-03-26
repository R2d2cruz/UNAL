import pygame


class NPC(pygame.sprite.Sprite):

    attack = 30
    defense = 20
    HP = 500
    xp = 0
    speed = 3
    velocity = [0, 0]
    x = 0
    y = 0

    def __init__(self, position, reference, name="Henry", *groups):
        super().__init__(*groups)
        self.name = name
        self.sheet = pygame.image.load(self.name + ".png")
        self.sheet.set_clip(pygame.Rect(37, 1, 34, 56))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.x = position[0]
        self.y = position[1]
        print(reference)
        self.change_reference_point(reference)
        self.frame = 0
        self.front = {0: (37, 1, 34, 56)}
        self.back = {0: (1, 1, 34, 56)}
        self.left = {0: (217, 1, 32, 56)}
        self.right = {0: (251, 1, 32, 56)}

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(clipped_rect)
        return clipped_rect

    def act(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def get_x(self):
        return self.rect.topleft[0]

    def get_y(self):
        return self.rect.topleft[1]

    def get_velocity(self):
        return self.velocity

    def collitions(self, objeto):
        pass

    def change_reference_point(self, position):
        self.rect.topleft = [self.x + position[0], self.y + position[1]]

    def get_rect(self):
        return pygame.Rect((self.x, self.y, 34, 56))
