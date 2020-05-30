from core.AnimatedEntity import AnimatedEntity
from core.SteeringBehavior import SteeringBehavior
from core.Vector2D import EPSILON, Vector2D, truncate, normalize


class MovingEntity(AnimatedEntity):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.steering = SteeringBehavior(self)
        self.mass = 50.0
        self.maxSpeed = .1
        self.maxForce = .1
        self.velocity = Vector2D(0.0, 0.0)
        self.heading = Vector2D(0.0, 1.0)
        self.speed = 0
        self.hasChanged = True
        self.x, self.y = position
        self.oldPos = Vector2D(self.x, self.y)

    def update(self, deltaTime: float):
        super().update(deltaTime)
        steeringForce = self.steering.calculate() 
        acceleration = Vector2D(steeringForce.x / self.mass, steeringForce.y / self.mass)

        self.velocity.x += acceleration.x * deltaTime
        self.velocity.y += acceleration.y * deltaTime
        self.velocity = truncate(self.velocity, self.maxSpeed)

        self.oldPos.x = self.x
        self.oldPos.y = self.y

        self.x += self.velocity.x * deltaTime
        self.y += self.velocity.y * deltaTime

        if self.velocity.isGtEpsilon():
            self.heading = normalize(self.velocity)
            self.hasChanged = True
            #self.side = perp(self.heading);

    def stop(self):
        self.velocity.setZero()
        self.x = self.oldPos.x
        self.y = self.oldPos.y
