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
        self.__velocity = Vector2D(0.0, 0.0)
        self.__steeringForce = Vector2D(0.0, 0.0)
        self.__acceleration = Vector2D(0.0, 0.0)
        self.steering = SteeringBehavior(self)
        self.__heading = Vector2D(0.0, 1.0)
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

    @property
    def velocity(self):
        return self.__velocity

    @property
    def heading(self):
        return self.__heading

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.__steeringForce = self.steering.calculate() 
        self.__acceleration = (self.__steeringForce / self.__mass)

        self.__velocity += (self.__acceleration * deltaTime)
        self.__velocity = truncate(self.__velocity, self.__maxSpeed)

        self.__oldPos.x = self.x
        self.__oldPos.y = self.y

        self.x += self.__velocity.x * deltaTime
        self.y += self.__velocity.y * deltaTime

        if self.__velocity.isGtEpsilon():
            self.hasChanged = True
            self.__heading = normalize(self.__velocity)
            #self.side = perp(self.heading);

    def render(self, screen, camera):
        super().render(screen, camera)
        # pygame.draw.line(screen, (255, 0, 0), camera.apply([self.x, self.y]), camera.apply([self.x + self.__steeringForce.x * 1000, self.y + self.__steeringForce.y * 1000]), 2)
        # pygame.draw.line(screen, (0, 255, 0), camera.apply([self.x, self.y + 10]), camera.apply([self.x + self.__acceleration.x * 1000, self.y + self.__acceleration.y * 1000 + 10]), 2)
        # pygame.draw.line(screen, (0, 0, 255), camera.apply([self.x, self.y + 20]), camera.apply([self.x + self.__velocity.x * 100, self.y + self.__velocity.y * 100 + 20]), 2)
        # pygame.draw.circle(screen, (0, 0, 0), camera.apply([self.x, self.y]), 100, 2)

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

    def getOldCollisionRect(self):
        return pygame.Rect((self.__oldPos.x, self.__oldPos.y + 24, 34, 32))

