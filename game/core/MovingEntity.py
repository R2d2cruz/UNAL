import pygame

from .misc import Colors
from .AnimatedEntity import AnimatedEntity
from .Entity import Entity
from .SteeringBehavior import SteeringBehavior
from .v2D import Vector2D, normalize, truncate


class MovingEntity(AnimatedEntity):
    def __init__(self, position, collissionRect, *groups):
        super().__init__(*groups)
        self.__mass = 10
        self.__maxSpeed = 0.25
        self.__maxForce = .018
        self.__velocity = Vector2D(0.0, 0.0)
        self.__steeringForce = Vector2D(0.0, 0.0)
        self.__acceleration = Vector2D(0.0, 0.0)
        self.__heading = Vector2D(0.0, 1.0)
        self.__collRect = pygame.Rect(collissionRect)
        self.__oldPos = Vector2D(position[0], position[1])
        self.__step = Vector2D()
        self.setPos(position[0], position[1])
        self.steering = SteeringBehavior(self)
        self.speed = 0
        self.hasChanged = True
        self.font = None
        self.world = None

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

    @maxSpeed.setter
    def maxSpeed(self, maxSpeed: float):
        self.__maxSpeed = maxSpeed

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

    def getOldPos(self):
        return self.__oldPos

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.__steeringForce = truncate(self.steering.calculate(), self.maxForce)
        self.__acceleration = (self.__steeringForce / self.__mass)
        self.__velocity += (self.__acceleration * deltaTime)
        self.__velocity = truncate(self.__velocity, self.__maxSpeed)
        self.x += self.__velocity.x * deltaTime
        self.y += self.__velocity.y * deltaTime
        self.__step = self.__velocity * deltaTime
        if self.__velocity.isGtEpsilon():
            self.hasChanged = True
            self.__heading = normalize(self.__velocity)
            # self.side = perp(self.heading);

    def render(self, surface, camera):
        super().render(surface, camera)
        # pygame.draw.circle(surface, Colors.BLACK, camera.apply([self.x, self.y]), 100, 2)
        # pygame.draw.circle(surface, Colors.BLACK, camera.apply([self.x, self.y]), 16, 2)
        # label = self.font.render(f" F {self.__steeringForce.length():.4f}", True, Colors.RED)
        # surface.blit(label, camera.apply([self.x + 20, self.y]))
        # pygame.draw.line(surface, Colors.RED, camera.apply([self.x, self.y]),
        #                  camera.apply([self.x + self.__steeringForce.x * 3000,
        #                                self.y + self.__steeringForce.y * 3000]), 2)
        #
        # label = self.font.render(f" a {self.__acceleration.length():.4f}", True, Colors.GREEN)
        # surface.blit(label, camera.apply([self.x + 20, self.y + 18]))
        # pygame.draw.line(surface, Colors.GREEN, camera.apply([self.x, self.y + 10]), camera.apply(
        #     [self.x + self.__acceleration.x * 3000, self.y + self.__acceleration.y * 3000 + 10]), 2)
        #
        # label = self.font.render(f" v {self.__velocity.length():.4f}", True, Colors.BLUE)
        # surface.blit(label, camera.apply([self.x + 20, self.y + 36]))
        # pygame.draw.line(surface, Colors.BLUE, camera.apply([self.x, self.y + 20]),
        #                  camera.apply([self.x + self.__velocity.x * 300, self.y + self.__velocity.y * 300 + 20]), 2)
        #
        # label = self.font.render(f"dX {self.__step.length():.4f}", True, (255, 200, 200))
        # surface.blit(label, camera.apply([self.x + 20, self.y + 54]))
        for feeler in self.steering.feelers:
            if feeler is not None:
                pygame.draw.line(surface, Colors.RED, camera.apply([self.x, self.y]),
                                 camera.apply([feeler.x, feeler.y]), 2)

    def stop(self, x: bool, y: bool):
        self.__velocity.setZero()
        if x:
            # self.__velocity.x -= self.__velocity.x * 1.01
            self.x = self.__oldPos.x
        if y:
            # self.__velocity.y -= self.__velocity.y * 1.01
            self.y = self.__oldPos.y

    def move(self, vector: Vector2D):
        self.steering.fixedForce = vector

    def setCollisionRect(self, collTuple):
        self.__collRect = pygame.Rect(collTuple)

    def getCollisionRect(self):
        collRect = self.__collRect.copy()
        collRect.center = (self.x, self.y)
        return collRect

    def getOldCollisionRect(self):
        collRect = self.__collRect.copy()
        collRect.center = (self.__oldPos.x, self.__oldPos.y)
        return collRect
