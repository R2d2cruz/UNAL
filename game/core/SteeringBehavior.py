import math
import random

# el radio limite para wander
from .v2D import getVector2D, normalize, Vector2D, distanceSq, rotateAroundOrigin, distance

WANDER_RADIUS = 1.2
# distancia de proyeccion del circulo de wnader frente a la entidad
WANDER_DIST = 10.0
# cambio de angulo
ANGLE_CHANGE = 1

DEFAULT_WEIGHT = 1.0

WallDetectionFeelerLength = 40
MaxDouble = 10000000000000


def randomClamped():
    return random.random() - random.random()


class SteeringBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.feelers = [None, None, None]

        self.wallAvoidanceWeight = DEFAULT_WEIGHT
        self.wallAvoidanceEnabled = True

        self.wanderAngle = random.random() * math.pi * 2
        self.wanderEnabled = False
        self.weightWander = DEFAULT_WEIGHT

        self.seekEnabled = False
        self.seekTarget = None
        self.weightSeek = DEFAULT_WEIGHT

        self.fleeEnabled = False
        self.fleeTarget = None
        self.weightFlee = DEFAULT_WEIGHT

        self.arriveEnabled = False
        self.arriveTarget = None
        self.arriveSlowRadius = 10.0
        self.weightArrive = DEFAULT_WEIGHT

        self.pursuitEnabled = False
        self.pursuitTarget = None
        self.weightPursuit = DEFAULT_WEIGHT

        self.offsetPursuitEnabled = False
        self.offsetPursuitTarget = None
        self.offsetPursuitDistance = None
        self.weightOffsetPursuit = DEFAULT_WEIGHT

        self.interposeEnabled = False
        self.interposeTargetA = None
        self.interposeTargetB = None
        self.weightInterpose = DEFAULT_WEIGHT

        self.hideEnabled = False
        self.hideTarget = None
        self.hideObtacles = None
        self.weightHide = DEFAULT_WEIGHT

        self.followPathEnabled = False
        self.followPathTarget = None
        self.weightFollowPath = DEFAULT_WEIGHT

    def resetAll(self):
        self.wanderAngle = random.random() * math.pi * 2
        self.wanderEnabled = False
        self.weightWander = DEFAULT_WEIGHT

        self.seekEnabled = False
        self.seekTarget = None
        self.weightSeek = DEFAULT_WEIGHT

        self.fleeEnabled = False
        self.fleeTarget = None
        self.weightFlee = DEFAULT_WEIGHT

        self.arriveEnabled = False
        self.arriveTarget = None
        self.arriveSlowRadius = 10.0
        self.weightArrive = DEFAULT_WEIGHT

        self.followPathEnabled = False
        self.followPathTarget = None
        self.weightFollowPath = DEFAULT_WEIGHT

        # self.pursuitEnabled = False
        # self.pursuitTarget = None
        # self.weightPursuit = DEFAULT_WEIGHT
        #
        # self.offsetPursuitEnabled = False
        # self.offsetPursuitTarget = None
        # self.offsetPursuitDistance = None
        # self.weightOffsetPursuit = DEFAULT_WEIGHT
        #
        # self.interposeEnabled = False
        # self.interposeTargetA = None
        # self.interposeTargetB = None
        # self.weightInterpose = DEFAULT_WEIGHT
        #
        # self.hideEnabled = False
        # self.hideTarget = None
        # self.hideObtacles = None
        # self.weightHide = DEFAULT_WEIGHT

    # retorna un vector para mover la entidad hacia la posicion dada
    def seek(self, target) -> Vector2D:
        agent = getVector2D(self.agent)
        vector = normalize(target - agent) * self.agent.maxSpeed
        return vector - self.agent.velocity

    # parecido a seek pero se detiene en el punto
    def arrive(self, target) -> Vector2D:
        agent = getVector2D(self.agent)
        vector = target - agent
        distanceToTarget = vector.length()

        if distanceToTarget < 5:
            self.followPathEnabled = False
            self.followPathTarget = None
            self.agent.velocity.setZero()
            return Vector2D(0, 0)

        vector = normalize(vector) * self.agent.maxSpeed
        # if distance < self.arriveSlowRadius:
        #     vector *= (distance / self.arriveSlowRadius)
        ramp = min(distanceToTarget / self.arriveSlowRadius, 1.0)
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
        lon = displacement.length()
        displacement = Vector2D(math.cos(self.wanderAngle), math.sin(self.wanderAngle)) * lon
        # cambiar el wanderAngle un poquito para la siguiente iteracion
        self.wanderAngle += random.random() * ANGLE_CHANGE - ANGLE_CHANGE * .5
        # calcular la fuerza
        return circleCenter + displacement

    # evadir varios obstaculos

    # @staticmethod
    # def obstacleAvoidance(obstacles: list) -> Vector2D:
    #     # the detection box length is proportional to the agent's velocity
    #     # m_dDBoxLength = Prm.MinDetectionBoxLength + (self.agent.Speed()/self.agent.MaxSpeed()) * Prm.MinDetectionBoxLength
    #     # tag all obstacles within range of the box for processing
    #     # this will keep track of the closest intersecting obstacle (CIB)
    #     closestIntersectingObstacle: Entity = None
    #     # this will be used to track the distance to the CIB
    #     distToClosestIP = MaxDouble
    #     # this will record the transformed local coordinates of the CIB
    #     localPosOfClosestObstacle: Vector2D = None
    #     for obstacle in obstacles:
    #         # calculate this obstacle's position in local space
    #         localPos = pointToLocalSpace(obstacle.getPos(), self.agent)
    #         # if the local position has a negative x value then it must lay
    #         # behind the agent. (in which case it can be ignored)
    #         if localPos.x >= 0:
    #             # if the distance from the x axis to the object's position is less
    #             # than its radius + half the width of the detection box then there
    #             # is a potential intersection.
    #             expandedRadius = obstacle.radius + self.agent.radius
    #             if fabs(localPos.y) < ExpandedRadius:
    #                 # now to do a line/circle intersection test. The center of the
    #                 # circle is represented by (cX, cY). The intersection points are
    #                 # given by the formula x = cX +/-sqrt(r^2-cY^2) for y=0.
    #                 # We only need to look at the smallest positive value of x because
    #                 # that will be the closest point of intersection.
    #                 cX = localPos.x
    #                 cY = localPos.y
    #
    #                 # we only need to calculate the sqrt part of the above equation once
    #                 double SqrtPart = sqrt(ExpandedRadius*ExpandedRadius - cY*cY)
    #
    #                 double ip = cX - SqrtPart
    #
    #                 if (ip <= 0.0)
    #                 {
    #                     ip = cX + SqrtPart
    #                 }
    #
    #                 # test to see if this is the closest so far. If it is keep a
    #                 # record of the obstacle and its local coordinates
    #                 if (ip < DistToClosestIP)
    #                 {
    #                     distToClosestIP = ip
    #
    #                     ClosestIntersectingObstacle = obstacle
    #                     localPosOfClosestObstacle = localPos
    #                 }
    #             }
    #         }
    #
    #     # if we have found an intersecting obstacle, calculate a steering force away from it
    #     force = Vector2D()
    #     if ClosestIntersectingObstacle:
    #         # the closer the agent is to an object, the stronger the
    #         # steering force should be
    #         double multiplier = 1.0 + (m_dDBoxLength - LocalPosOfClosestObstacle.x) / m_dDBoxLength
    #         # calculate the lateral force
    #         SteeringForce.y = (ClosestIntersectingObstacle->BRadius() -  LocalPosOfClosestObstacle.y)  * multiplier
    #         # apply a braking force proportional to the obstacles distance from the vehicle.
    #         const double BrakingWeight = 0.2
    #         SteeringForce.x = (ClosestIntersectingObstacle->BRadius() - LocalPosOfClosestObstacle.x) *  BrakingWeight
    #
    #     # finally, convert the steering vector from local to world space
    #     return VectorToWorldSpace(force, self.agent.heading, self.agent.Side())

    # evadir paredes
    # def wallAvoidance(self, walls: list) -> Vector2D:
    #     self.createFeelers()
    #     distToThisIP = 0.0
    #     distToClosestIP = MaxDouble
    #     closestWall = None
    #     force = Vector2D()
    #     point = Vector2D()
    #     closestPoint = Vector2D()
    #
    #     for feeler in self.feelers:
    #         for wall in walls:
    #             intersection = LineIntersection2D(
    #                 self.agent.getPos(), feeler, wall.From(), wall.To())
    #             if intersection[0]:
    #                 distToThisIP = intersection[1]
    #                 distToClosestIP = intersection[2]
    #                 if distToThisIP < distToClosestIP:
    #                     distToClosestIP = distToThisIP
    #                     closestWall = wall
    #                     closestPoint = intersection[3]
    #
    #         if closestWall is not None:
    #             overShoot = feeler - closestPoint
    #             force = wall.Normal() * overShoot.Length()
    #
    #     return force

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

    def accumulateForce(self, runningTot: list, forceToAdd: Vector2D):
        magnitudeSoFar = runningTot[0].length()
        magnitudeRemaining = self.agent.maxForce - magnitudeSoFar
        if magnitudeRemaining <= 0.0:
            return False

        magnitudeToAdd = forceToAdd.length()
        if magnitudeToAdd < magnitudeRemaining:
            runningTot[0] += forceToAdd
        else:
            runningTot[0] += normalize(forceToAdd) * magnitudeRemaining

        return True

    # la suma de todas las fuerzas que operan sobre la entidad
    def calculate(self) -> Vector2D:
        steering = [Vector2D()]

        # if self.wallAvoidanceEnabled:
        #     force = self.wallAvoidance(self.agent.world.walls) * self.wallAvoidanceWeight
        #     if not self.accumulateForce(steering, force):
        #         return steering[0]

        # if self.obstacleAvoidanceEnabled:
        #     force = self.obstacleAvoidance(self.target.world.obstacles) * self.obstacleAvoidanceWeight
        #     if not self.accumulateForce(steering, force):
        #         return steering

        if self.wanderEnabled:
            force = self.wander() * self.weightWander
            if not self.accumulateForce(steering, force):
                return steering[0]

        if self.seekEnabled:
            force = self.seek(getVector2D(self.seekTarget)) * self.weightSeek
            if not self.accumulateForce(steering, force):
                return steering[0]

        if self.fleeEnabled:
            force = self.flee(getVector2D(self.fleeTarget)) * self.weightFlee
            if not self.accumulateForce(steering, force):
                return steering[0]

        if self.arriveEnabled:
            force = self.arrive(getVector2D(self.arriveTarget)) * self.weightArrive
            if not self.accumulateForce(steering, force):
                return steering[0]

        # if self.pursuitEnabled:
        #     # assert(self.pursuitTarget && "pursuit target not assigned")
        #     steering += self.pursuit(self.pursuitTarget) * self.weightPursuit

        # if self.offsetPursuitEnabled:
        #     # assert (self.offsetPursuitTarget && "pursuit target not assigned")
        #     # assert (not self.offsetPursuitDistance.isZero() && "No offset assigned")
        #     steering += self.offsetPursuit(self.offsetPursuitTarget,
        #                                    self.offsetPursuitDistance) * self.weightOffsetPursuit

        # if self.interposeEnabled:
        #     # assert (self.interposeTargetA && self.interposeTargetB && "Interpose agents not assigned")
        #     steering += self.interpose(self.interposeTargetA,
        #                                self.interposeTargetB) * self.weightInterpose

        # if self.hideEnabled:
        #     # assert(self.hideTarget && "Hide target not assigned")
        #     steering += self.hide(self.hideTarget,
        #                           self.hideObtacles) * self.weightHide

        if self.followPathEnabled:
            force = self.followPath() * self.weightFollowPath
            if not self.accumulateForce(steering, force):
                return steering[0]

        return steering[0]

    def createFeelers(self):
        speed = self.agent.velocity.length()
        halfPi = math.pi / 2.0
        # crea un palpador al frente
        self.feelers[0] = self.agent.getPos() + self.agent.heading * WallDetectionFeelerLength

        # crea un palpador a la izquierda
        temp = self.agent.heading.copy()
        rotateAroundOrigin(temp, halfPi * 3.5)
        self.feelers[1] = self.agent.getPos() + temp * (WallDetectionFeelerLength / 2.0)

        # crea un palpador a la derecha
        temp = self.agent.heading.copy()
        rotateAroundOrigin(temp, halfPi * 0.5)
        self.feelers[2] = self.agent.getPos() + temp * (WallDetectionFeelerLength / 2.0)


"""



"""
