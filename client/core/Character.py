import pygame


class Character(pygame.sprite.Sprite):
    def blit(self, screen):
        #pygame.draw.rect(screen, (0, 255, 0), self.get_rect())
        screen.blit(self.image, self.rect)

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

    def get_velocity(self):
        return self.velocity