from core.AnimatedEntity import AnimatedEntity
from core.SteeringBehavior import SteeringBehavior


def truncate(velocity, maxSpeed):
    return velocity


class MovingEntity(AnimatedEntity):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.__steering = SteeringBehavior()
        self.__steeringOn = False
        self.maxSpeed = 1
        self.velocity = [0, 0]
        self.speed = 4

    def update(self, deltaTime: float):
        super().update(deltaTime)
        if self.__steeringOn:
            steeringForce = self.__steering.calculate()
            # acceleration = steeringForce / mass
            #  self.velocity += acceleration * deltaTime
            # la masa no nos importa, asumimos que la masa es 1
            self.velocity += steeringForce * deltaTime
            self.velocity = truncate(self.velocity, self.maxSpeed)
