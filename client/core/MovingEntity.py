from core.AnimatedEntity import AnimatedEntity
from core.SteeringBehavior import SteeringBehavior
from core.Vector2D import EPSILON, Vector2D, truncate, normalize


class MovingEntity(AnimatedEntity):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.__steering = SteeringBehavior()
        self.maxSpeed = 1
        self.velocity = Vector2D(0.0, 0.0)
        self.oldPos = Vector2D(0.0, 0.0)
        self.heading = Vector2D(0.0, 1.0)
        self.speed = 0

    def update(self, deltaTime: float):
        super().update(deltaTime)
        seconds = deltaTime / 20
        steeringForce = self.__steering.calculate() 
        # acceleration = steeringForce / mass
        #  self.velocity += acceleration * deltaTime
        # la masa no nos importa, asumimos que la masa es 1
        self.velocity.x += steeringForce.x * seconds
        self.velocity.y += steeringForce.y * seconds
        self.velocity = truncate(self.velocity, self.maxSpeed)
        self.oldPos = [self.x, self.y]
        self.x += self.velocity.x * seconds
        self.y += self.velocity.y * seconds
        if self.velocity.isGtEpsilon():
            self.heading = normalize(self.velocity)
            self.hasChanged = True
            #self.side = perp(self.heading);

    def stop(self):
        self.velocity.setZero()
        self.x = self.oldPos[0]
        self.y = self.oldPos[1]
