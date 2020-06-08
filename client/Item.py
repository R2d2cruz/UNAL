import pygame
from core.Entity import Entity
from core.Vector2D import Vector2D
from Player import Player
import core.ResourceManager as res
import client.core.EntityManager as entManager
import core.Hermes as Hermes
from core.Telegram import Telegram

MAXYINTERVAL = 6


class Item(Entity):
    def __init__(self, name: str, rect: pygame.Rect, positionCenter: Vector2D):
        self.name = name
        self.image = res.loadImage(self.name, rect)
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

    def effect(self, player) -> bool:
        pass


# 16 8 40 48

class HealthPotion(Item):
    def __init__(self, name: str, rect: tuple, position: Vector2D, healPower: int):
        super().__init__(name, pygame.Rect(rect), position)
        self.healPower = healPower
        self.effect = self.recoveryHealth

    def recoveryHealth(self, player: Player):
        Hermes.messageDispatch(0, self.id, player.id, "heal", {"medicine": self.healPower})
        return True

    def onMessage(self, telegram: Telegram):
        if telegram.message == "youHealMe":
            # eliminar este item
            pass
