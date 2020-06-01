import pygame
from core.AnimatedEntity import AnimatedEntity
from core.SteeringBehavior import SteeringBehavior
from core.Vector2D import EPSILON, Vector2D, truncate, normalize


class MovingEntity(AnimatedEntity):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.steering = SteeringBehavior(self)
        self.mass = 100
        self.maxSpeed = .2
        self.maxForce = .05
        self.steeringForce = Vector2D(0.0, 0.0)
        self.acceleration = Vector2D(0.0, 0.0)
        self.velocity = Vector2D(0.0, 0.0)
        self.heading = Vector2D(0.0, 1.0)
        self.speed = 0
        self.hasChanged = True
        self.x, self.y = position
        self.oldPos = Vector2D(self.x, self.y)
        #self.isInCollision = False

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.steeringForce = self.steering.calculate() 
        self.acceleration = (self.steeringForce / self.mass)

        self.velocity += (self.acceleration * deltaTime)
        self.velocity = truncate(self.velocity, self.maxSpeed)

        self.oldPos.x = self.x
        self.oldPos.y = self.y

        self.x += self.velocity.x * deltaTime
        self.y += self.velocity.y * deltaTime

        if self.velocity.isGtEpsilon():
            self.heading = normalize(self.velocity)
            self.hasChanged = True
            #self.side = perp(self.heading);

    def stop(self, x: bool, y: bool):
        print(x)
        if x:
            self.velocity.x = 0
            self.x = self.oldPos.x

        if y:
            self.velocity.y = 0
            self.y = self.oldPos.y

    def getOldCollisionRect(self):
        return pygame.Rect((self.oldPos.x, self.oldPos.y + 24, 34, 32))

        # self.velocity.setZero()
        # self.x = self.oldPos.x
        # self.y = self.oldPos.y
