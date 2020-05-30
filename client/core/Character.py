import json
import pygame
import core.ResourceManager as res
from core.MovingEntity import MovingEntity


compassClips = ['right', 'down', 'down', 'down', 'left', 'up', 'up', 'up']
traductor = {
    "stand_up": "stu",
    "stand_down": "std",
    "stand_left": "stl",
    "stand_right": "str",
    "up": "wlu",
    "down": "wld",
    "left": "wll",
    "right": "wlr"
}
maxHealt = 100


class Character(MovingEntity):
    def __init__(self, name: str, animationName: str, position, *groups):
        super().__init__(position, *groups)
        self.__color = (0, 0, 0)
        self.__nameSurface = None
        self.__nameRect = None
        self.setName(name)
        self.animName = animationName
        self.loadAnimation(res.getAnimFile(self.animName))
        self.__health = 100
        self.attack = 30
        self.defense = 20

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.__nameRect.x, self.__nameRect.y = (
            self.x + (34 - self.__nameRect.width) / 2, self.y - 14)
        direction = compassClips[self.heading.getCompass()]
        self.currentClip = (
            'stand_' if self.velocity.isZero() else '') + direction

    def render(self, screen, camera):
        super().render(screen, camera)
        if self.name is not None:
            if self.__nameSurface is not None:
                screen.blit(self.__nameSurface, camera.apply(self.__nameRect))
        if camera is not None:
            pygame.draw.rect(screen, (255 * (1 - self.health / maxHealt), 255 * self.health / maxHealt, 0, 0.4),
                             camera.apply(self.getHealthRect()))
            pygame.draw.rect(screen, (0, 0, 0, 0.4), camera.apply(self.getHealthEmptyRect()), 1)
        else:
            pygame.draw.rect(screen, (255 * (1 - self.health / maxHealt), 255 * self.health / maxHealt, 0, 0.2),
                             self.getHealthRect())
            pygame.draw.rect(screen, (0, 0, 0, 0.2), self.getHealthEmptyRect(), 1)

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=traductor.get(self.currentClip)
        )

    def setName(self, name: str):
        if name is not None or name != '':
            self.name = name
            font = res.getFont('minecraft', 14)
            self.__nameSurface, self.__nameRect = res.getText(
                self.name, font, self.__color)
        else:
            self.__nameSurface = None
            self.__nameRect = None
            self.name = None

    def getHealthRect(self):
        return pygame.Rect(self.x + (self.width / 2) - 20, self.y + self.height + 4, 40 * self.health / maxHealt, 8)

    def getHealthEmptyRect(self):
        return pygame.Rect(self.x + (self.width / 2) - 20, self.y + self.height + 4, 40, 8)

    def collitions(self, rect: pygame.Rect):
        pass

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        if health <= maxHealt:
            self.__health = health

    def damage(self, damage=5):
        self.health -= damage

    def heal(self, medicine):
        self.health += medicine
