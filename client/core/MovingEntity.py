import pygame
from core.AnimatedEntity import AnimatedEntity
from core.SteeringBehavior import SteeringBehavior
from core.Vector2D import EPSILON, Vector2D, truncate, normalize


class MovingEntity(AnimatedEntity):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.x, self.y = position
        self.__oldPos = Vector2D(self.x, self.y)
        self.__mass = 100
        self.__maxSpeed = .2
        self.__maxForce = .05
        self.steering = SteeringBehavior(self)
        self.steeringForce = Vector2D(0.0, 0.0)
        self.acceleration = Vector2D(0.0, 0.0)
        self.velocity = Vector2D(0.0, 0.0)
        self.heading = Vector2D(0.0, 1.0)
        self.speed = 0
        self.hasChanged = True
        #self.isInCollision = False

    @property
    def mass(self):
        return self.__mass

    @property
    def maxSpeed(self):
        return self.__maxSpeed

    @property
    def maxForce(self):
        return self.__maxForce

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.steeringForce = self.steering.calculate() 
        self.acceleration = (self.steeringForce / self.__mass)

        self.velocity += (self.acceleration * deltaTime)
        self.velocity = truncate(self.velocity, self.__maxSpeed)

        self.__oldPos.x = self.x
        self.__oldPos.y = self.y

        self.x += self.velocity.x * deltaTime
        self.y += self.velocity.y * deltaTime

        if self.velocity.isGtEpsilon():
            self.heading = normalize(self.velocity)
            self.hasChanged = True
            #self.side = perp(self.heading);

    def render(self, screen, camera):
        super().render(screen, camera)
        # pygame.draw.line(screen, (255, 0, 0), camera.apply([self.x, self.y]), camera.apply([self.x + self.steeringForce.x * 1000, self.y + self.steeringForce.y * 1000]), 2)
        # pygame.draw.line(screen, (0, 255, 0), camera.apply([self.x, self.y + 10]), camera.apply([self.x + self.acceleration.x * 1000, self.y + self.acceleration.y * 1000 + 10]), 2)
        # pygame.draw.line(screen, (0, 0, 255), camera.apply([self.x, self.y + 20]), camera.apply([self.x + self.velocity.x * 100, self.y + self.velocity.y * 100 + 20]), 2)
        # pygame.draw.circle(screen, (0, 0, 0), camera.apply([self.x, self.y]), 100, 2)

    def stop(self, x: bool, y: bool):
        # self.velocity.setZero()
        if x:
            self.velocity.x = 0
            self.x = self.__oldPos.x
        if y:
            self.velocity.y = 0
            self.y = self.__oldPos.y

    def getOldCollisionRect(self):
        return pygame.Rect((self.__oldPos.x, self.__oldPos.y + 24, 34, 32))

