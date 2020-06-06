import pygame
import core.ResourceManager as res
from core.MovingEntity import MovingEntity
from core.Telegram import Telegram


compassClips = ['right', 'down', 'down', 'down', 'left', 'up', 'up', 'up']
translate = {
    "stand_up": "stu",
    "stand_down": "std",
    "stand_left": "stl",
    "stand_right": "str",
    "up": "wlu",
    "down": "wld",
    "left": "wll",
    "right": "wlr"
}
maxHealth = 100


class Character(MovingEntity):
    def __init__(self, name: str, animationName: str, position, *groups):
        super().__init__(position, *groups)
        self.__color = (0, 0, 0)
        self.__nameSurface = None
        self.__nameRect = None
        self.name = None
        self.setName(name)
        self.animName = animationName
        self.loadAnimation(res.getAnimFile(self.animName))
        self.__health = 100
        self.attack = 30
        self.defense = 20
        if not self.onMessage:
            self.switchMessage()

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.__nameRect.x, self.__nameRect.y = (
            self.x + (34 - self.__nameRect.width) / 2, self.y - 14)
        direction = compassClips[self.heading.getCompass()]
        self.currentClip = (
            'stand_' if self.velocity.isZero() else '') + direction

    def stop(self, x, y):
        super().stop(x, y)
        self.__nameRect.x, self.__nameRect.y = (
            self.x + (34 - self.__nameRect.width) / 2, self.y - 14)

    def render(self, screen, camera):
        super().render(screen, camera)
        if self.name is not None:
            if self.__nameSurface is not None:
                screen.blit(self.__nameSurface, camera.apply(self.__nameRect))
        if self.health != maxHealth:
            pygame.draw.rect(screen, (255 * (1 - self.health / maxHealth), 255 * self.health / maxHealth, 0, 0.4),
                             camera.apply(self.getHealthRect()))
            pygame.draw.rect(screen, (0, 0, 0, 0.4), camera.apply(self.getHealthEmptyRect()), 1)

        # pygame.draw.line(screen, (255, 0, 0), camera.apply([self.x, self.y]), camera.apply([self.x + self.steeringForce.x * 1000, self.y + self.steeringForce.y * 1000]), 2)
        # pygame.draw.line(screen, (0, 255, 0), camera.apply([self.x, self.y + 10]), camera.apply([self.x + self.acceleration.x * 1000, self.y + self.acceleration.y * 1000 + 10]), 2)
        # pygame.draw.line(screen, (0, 0, 255), camera.apply([self.x, self.y + 20]), camera.apply([self.x + self.velocity.x * 100, self.y + self.velocity.y * 100 + 20]), 2)
        # pygame.draw.circle(screen, (0, 0, 0), camera.apply([self.x, self.y]), 100, 2)

        if self.steering.followPathTarget is not None:
            self.steering.followPathTarget.render(screen, camera)

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=translate.get(self.currentClip)
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
        return pygame.Rect(self.x + (self.width / 2) - 20, self.y + self.height + 4, 40 * self.health / maxHealth, 8)

    def getHealthEmptyRect(self):
        return pygame.Rect(self.x + (self.width / 2) - 20, self.y + self.height + 4, 40, 8)

    def getCollisionRect(self):
        return pygame.Rect((self.x, self.y + 24, 34, 32))

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        if health <= maxHealth:
            self.__health = health

    def damage(self, damage=5):
        self.health -= damage

    def heal(self, medicine):
        self.health += medicine

    def onHandleMessages(self, telegram: Telegram):
        # estraer toda la informacion de telegram
        pass
