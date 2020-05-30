import pygame
from core.Character import Character


class NPC(Character):
    attack = 30
    defense = 20
    HP = 500
    xp = 0

    def get_rect(self):
        return pygame.Rect((self.rect.x, self.rect.y + 32, 34, 32))

