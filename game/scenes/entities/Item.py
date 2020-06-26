import pygame

from ...core import (Entity, Telegram, Vector2D, hermes,
                     resourceManager)

MAXYINTERVAL = 6


class Item(Entity):
    def __init__(self, name: str, rect: pygame.Rect, positionCenter: Vector2D):
        super().__init__()
        self.name = name
        self.image = resourceManager.loadImage(self.name, rect)
        self.rect = rect
        self.x = positionCenter.x - self.rect.w
        self.y = positionCenter.y - self.rect.h
        self.direction = -1
        self.lastFrameTime = 0
        self.moveY = 0
        self.timeStep = 100
        self.flag = "item"

    def update(self, deltaTime: float):
        self.lastFrameTime += deltaTime
        if self.lastFrameTime >= self.timeStep:
            self.lastFrameTime -= self.timeStep
            self.moveY += 1
            self.y += self.direction
            if self.moveY >= MAXYINTERVAL:
                self.direction *= -1
                self.moveY = 0

    def onMessage(self, telegram: Telegram):
        pass

    def effect(self, player: Entity) -> bool:
        pass


class Book(Item):
    def __init__(self, name: str, position: Vector2D, data: dict, rect: tuple = (12, 12, 32, 40)):
        super().__init__(name, pygame.Rect(rect), position)
        if data is None:
            data = dict(
                tittle=name,
                text='',
                especial=None
            )
        self.isOn = True
        self.effect = self.collect
        self.data = data
        self.type = "item"

    def collect(self, entity):
        if self.isOn:
            print('collected')
            entity.collectBook(self.data)
            hermes.messageDispatch(0, self.id, hermes.worldId, 'deleteMe')


# 16 8 40 48

class HealthPotion(Item):
    def __init__(self, name: str, position: Vector2D, healPower: int, rect: tuple = (3, 2, 10, 12)):
        super().__init__(name, pygame.Rect(rect), position)
        self.healPower = healPower
        self.effect = self.recoveryHealth
        self.isOn = True
        self.type = "item"

    def recoveryHealth(self, player):
        if self.isOn:
            if player.heal(self.healPower):
                print('healed')
                hermes.messageDispatch(0, self.id, hermes.worldId, 'deleteMe')
            # hermes.messageDispatch(0, self.id, player.id, "heal", {"medicine": self.healPower})
        return True
