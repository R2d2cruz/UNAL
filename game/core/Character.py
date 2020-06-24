import pygame

from .Hermes import hermes
from .MovingEntity import MovingEntity
from .ResourceManager import resourceManager
from .Telegram import Telegram
from .camera.BaseCamera import BaseCamera
from .misc import getText

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
    def __init__(self, name: str, animationName: str, position, collisionRect, *groups):
        super().__init__(position, collisionRect, *groups)
        self.currentClip = None
        self.__color = (0, 0, 0)
        self.__nameSurface = None
        self.__nameRect = None
        self.name = None
        self.setName(name)
        self.animName = animationName
        self.loadAnimation(resourceManager.getAnimFile(self.animName))
        self.__health = 100
        self.__attack = 30
        self.__defense = 20
        self.type = 'character'

    @property
    def defense(self):
        return self.__defense

    @property
    def attackPower(self):
        return self.__attack

    def updateNameRect(self):
        self.__nameRect.x = self.x - self.__nameRect.w / 2
        self.__nameRect.y = self.rect.top - self.__nameRect.h

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.updateNameRect()
        direction = compassClips[self.heading.getCompass()]
        self.currentClip = ('stand_' if self.velocity.isZero() else '') + direction

    def stop(self, x, y):
        super().stop(x, y)
        self.updateNameRect()

    def render(self, surface, camera: BaseCamera):
        super().render(surface, camera)
        self.renderHealthBar(surface, camera)
        if (self.name is not None) and (self.__nameSurface is not None):
            surface.blit(self.__nameSurface, camera.apply(self.__nameRect))
        if self.steering.followPathTarget is not None:
            self.steering.followPathTarget.render(surface, camera)

    def renderHealthBar(self, surface, camera):
        if self.health != maxHealth:
            barWidth = 40
            healthValue = self.health / maxHealth
            healthColor = (int(255 * (1 - healthValue)), int(255 * healthValue), 0)
            x = self.x - barWidth / 2
            y = self.rect.bottom + 4
            pygame.draw.rect(surface, healthColor, camera.apply(pygame.Rect(x, y, barWidth * healthValue, 8)))
            pygame.draw.rect(surface, (0, 0, 0), camera.apply(pygame.Rect(x, y, barWidth, 8)), 1)

    def toDict(self):
        return dict(
            x=self.x,
            y=self.y,
            a=translate.get(self.currentClip)
        )

    def setName(self, name: str):
        if name is not None or name != '':
            self.name = name
            font = resourceManager.getFont('minecraft', 14)
            self.__nameSurface, self.__nameRect = getText(
                self.name, font, self.__color)
        else:
            self.__nameSurface = None
            self.__nameRect = None
            self.name = None

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

    def damage(self, damage=5):
        self.__health -= damage

    def heal(self, medicine):
        if self.health <= maxHealth:
            if self.health + medicine < maxHealth:
                self.__health += medicine
            else:
                self.__health = maxHealth
            return True
        else:
            return False

    def onMessage(self, telegram: Telegram) -> bool:
        if telegram.message == "heal":
            if self.heal(telegram.extraInfo.get("medicine")):
                hermes.messageDispatch(0, self.id, telegram.sender, "youHealMe", {})
                return True
        hermes.messageDispatch(0, self.id, telegram.sender, "IAlreadyHealed", {})
        return False
