import pygame
from core.Entity import Entity
from core.AnimatedEntity import AnimatedEntity
from core.SteeringBehavior import SteeringBehavior
from core.Vector2D import EPSILON, Vector2D, normalize, truncate


class MovingEntity(AnimatedEntity):
    def __init__(self, position, collissionRect, *groups):
        super().__init__(*groups)
        self.rect.centerx, self.rect.centery = position
        self.__oldPos = Vector2D(self.rect.centerx, self.rect.centery)
        self.__mass = 100
        self.__maxSpeed = 0.15
        self.__maxForce = .02
        self.__velocity = Vector2D(0.0, 0.0)
        self.__steeringForce = Vector2D(0.0, 0.0)
        self.__acceleration = Vector2D(0.0, 0.0)
        self.__heading = Vector2D(0.0, 1.0)
        self.__collRect = pygame.Rect(collissionRect)
        self.steering = SteeringBehavior(self)
        self.speed = 0
        self.hasChanged = True

    @Entity.x.setter
    def x(self, x):
        self.__oldPos.x = self.x
        self._Entity__pos.x = x
        self.rect.x = self.x - self.__collRect.x - self.__collRect.w / 2

    @Entity.y.setter
    def y(self, y):
        self.__oldPos.y = self.y
        self._Entity__pos.y = y
        self.rect.y = self.y - self.__collRect.y - self.__collRect.h / 2

    @property
    def mass(self):
        return self.__mass

    @property
    def maxSpeed(self):
        return self.__maxSpeed

    @property
    def maxForce(self):
        return self.__maxForce

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, vector: Vector2D):
        self.__velocity = vector

    @property
    def heading(self):
        return self.__heading

    def setPos(self, x: float, y: float):
        self.x, self.y = x, y

    def getPos(self):
        return self.__pos

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.__steeringForce = self.steering.calculate() 
        self.__acceleration = (self.__steeringForce / self.__mass)
        self.__velocity += (self.__acceleration * deltaTime)
        self.__velocity = truncate(self.__velocity, self.__maxSpeed)      
        self.x += self.__velocity.x * deltaTime
        self.y += self.__velocity.y * deltaTime
        if self.__velocity.isGtEpsilon():
            self.hasChanged = True
            self.__heading = normalize(self.__velocity)
            #self.side = perp(self.heading);

    def render(self, screen, camera):
        super().render(screen, camera)
        pygame.draw.line(screen, (255, 0, 0), camera.apply([self.x, self.y]), camera.apply([self.x + self.__steeringForce.x * 1000, self.y + self.__steeringForce.y * 1000]), 2)
        pygame.draw.line(screen, (0, 255, 0), camera.apply([self.x, self.y + 10]), camera.apply([self.x + self.__acceleration.x * 1000, self.y + self.__acceleration.y * 1000 + 10]), 2)
        pygame.draw.line(screen, (0, 0, 255), camera.apply([self.x, self.y + 20]), camera.apply([self.x + self.__velocity.x * 100, self.y + self.__velocity.y * 100 + 20]), 2)
        pygame.draw.circle(screen, (0, 0, 0), camera.apply([self.x, self.y]), 100, 2)
        pygame.draw.circle(screen, (0, 0, 0), camera.apply([self.x, self.y]), 16, 2)

    def stop(self, x: bool, y: bool):
        # self.__velocity.setZero()
        if x:
            self.__velocity.x = 0
            self.x = self.__oldPos.x
        if y:
            self.__velocity.y = 0
            self.y = self.__oldPos.y

    def move(self, vector: Vector2D):
        self.steering.fixedForce = vector

    def getCollisionRect(self):
        collRect = pygame.Rect(self.__collRect)
        collRect.center = (self.x, self.y)
        return collRect

    def getOldCollisionRect(self):
        collRect = pygame.Rect(self.__collRect)
        collRect.center = (self.__oldPos.x, self.__oldPos.y)
        return collRect
