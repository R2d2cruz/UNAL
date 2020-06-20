import math
import random

from .Vector2D import (Vector2D, distance, distanceSq, getVector2D,
                       normalize)

# el radio limite para wander
WANDER_RADIUS = 1.2
# distancia de proyeccion del circulo de wnader frente a la entidad
WANDER_DIST = 2.0
# cambio de angulo
ANGLE_CHANGE = 1


def randomClamped():
    return random.random() - random.random()


class SteeringBehavior:
    def __init__(self, agent):
        self.wanderAngle = random.random() * math.pi * 2
        self.agent = agent

        self.wanderEnabled = False
        self.weightWander = 1.0

        self.seekEnabled = False
        self.seekTarget = None
        self.weightSeek = 1.0

        self.fleeEnabled = False
        self.fleeTarget = None
        self.weightFlee = 1.0

        self.arriveEnabled = False
        self.arriveTarget = None
        self.arriveSlowRadius = 100.0
        self.weightArrive = 1.0

        self.pursuitEnabled = False
        self.pursuitTarget = None
        self.weightPursuit = 1.0

        self.offsetPursuitEnabled = False
        self.offsetPursuitTarget = None
        self.offsetPursuitDistance = None
        self.weightOffsetPursuit = 1.0

        self.interposeEnabled = False
        self.interposeTargetA = None
        self.interposeTargetB = None
        self.weightInterpose = 1.0

        self.hideEnabled = False
        self.hideTarget = None
        self.hideObtacles = None
        self.weightHide = 1.0

        self.followPathEnabled = False
        self.followPathTarget = None
        self.weightFollowPath = 1.0

    # retorna un vector para mover la entidad hacia la posicion dada
    def seek(self, target) -> Vector2D:
        agent = getVector2D(self.agent)
        vector = normalize(target - agent) * self.agent.maxSpeed
        return vector - self.agent.velocity

    # parecido a seek pero se detiene en el punto
    def arrive(self, target) -> Vector2D:
        agent = getVector2D(self.agent)
        vector = target - agent
        distance = vector.length()
        vector = normalize(vector) * self.agent.maxSpeed
        # if distance < self.arriveSlowRadius:
        #     vector *= (distance / self.arriveSlowRadius)
        ramp = min(distance / self.arriveSlowRadius, 1.0)
        # return vector - self.agent.velocity
        return (vector * ramp) - self.agent.velocity

    # retorna un vector para mover la entidad lejos de la posicion dada y con una distancia de panico especifica
    def flee(self, target) -> Vector2D:
        agent = getVector2D(self.agent)
        panicDistanceSq = 100.0 * 100.0
        if distanceSq(agent, target) > panicDistanceSq:
            return Vector2D(0, 0)
        vector = normalize(target - agent) * self.agent.maxSpeed
        return self.agent.velocity - vector

    # predice donde estara la entidad y retorna el seek hacia ese punto
    @staticmethod
    def pursuit(entity) -> Vector2D:
        pass

    # persigue  anteniendo una distancia
    @staticmethod
    def offsetPursuit(entity, offset) -> Vector2D:
        pass

    # evadir una entidad
    @staticmethod
    def evade(entity) -> Vector2D:
        pass

    # el wander que tanto necesitas hijo
    def wander(self) -> Vector2D:
        # calcular centro del circulo
        circleCenter = normalize(Vector2D(self.agent.velocity.x, self.agent.velocity.y)) * WANDER_DIST
        # calcular fuerza de desplacamiento
        displacement = Vector2D(0, -WANDER_RADIUS)
        # cambiar la direccioncambiando el angulo
        l = displacement.length()
        displacement = Vector2D(math.cos(self.wanderAngle), math.sin(self.wanderAngle)) * l
        # cambiar el wanderAngle un poquito para la siguiente iteracion
        self.wanderAngle += random.random() * ANGLE_CHANGE - ANGLE_CHANGE * .5
        # calcular la fuerza
        return circleCenter + displacement

    # evadir varios obstaculos

    @staticmethod
    def obstacleAvoidance(obstacles: list) -> Vector2D:
        pass

    # evadir paredes
    @staticmethod
    def wallAvoidance(walls) -> Vector2D:
        pass

    # seguir una ruta
    def followPath(self) -> Vector2D:
        target = self.followPathTarget.getCurrentWayPoint()
        dist = distance(target, getVector2D(self.agent))
        if self.followPathTarget.isFinished():
            if dist < 5:
                self.followPathEnabled = False
                self.followPathTarget = None
                self.agent.velocity.setZero()
                return Vector2D(0, 0)
            else:
                return self.arrive(target)
        else:
            if dist < 20:
                self.followPathTarget.setNextPoint()
                target = self.followPathTarget.getCurrentWayPoint()
            return self.seek(target)

    # interponerse entre dos entidades
    @staticmethod
    def interpose(entityA, entityB) -> Vector2D:
        pass

    # se oculta de otra entidad tras los obstculos dados
    @staticmethod
    def hide(hunter, obstacles) -> Vector2D:
        pass

    # la suma de todas las fuerzas que operan sobre la entidad
    def calculate(self) -> Vector2D:
        steering = Vector2D()
        if self.wanderEnabled:
            steering += self.wander() * self.weightWander
        if self.seekEnabled:
            steering += self.seek(getVector2D(self.seekTarget)) * self.weightSeek
        if self.fleeEnabled:
            steering += self.flee(getVector2D(self.fleeTarget)) * self.weightFlee
        if self.arriveEnabled:
            steering += self.arrive(getVector2D(self.arriveTarget)) * self.weightArrive

        # if self.pursuitEnabled:
        #     # assert(self.pursuitTarget && "pursuit target not assigned");
        #     steering += self.pursuit(self.pursuitTarget) * self.weightPursuit

        # if self.offsetPursuitEnabled:
        #     # assert (self.offsetPursuitTarget && "pursuit target not assigned");
        #     # assert (not self.offsetPursuitDistance.isZero() && "No offset assigned");
        #     steering += self.offsetPursuit(self.offsetPursuitTarget,
        #                                    self.offsetPursuitDistance) * self.weightOffsetPursuit

        # if self.interposeEnabled:
        #     # assert (self.interposeTargetA && self.interposeTargetB && "Interpose agents not assigned");
        #     steering += self.interpose(self.interposeTargetA,
        #                                self.interposeTargetB) * self.weightInterpose

        # if self.hideEnabled:
        #     # assert(self.hideTarget && "Hide target not assigned");
        #     steering += self.hide(self.hideTarget,
        #                           self.hideObtacles) * self.weightHide

        if self.followPathEnabled:
            steering += self.followPath() * self.weightFollowPath

        return steering
