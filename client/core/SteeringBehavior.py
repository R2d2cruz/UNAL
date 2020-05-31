import math
import random
from core.Vector2D import Vector2D, normalize, truncate, distanceSq, EPSILON, getVector2D


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
        self.weightFollowPath = 1.0

    # retorna un vector para mover la entidad hacia la posicion dada
    def seek(self) -> Vector2D:
        target = getVector2D(self.seekTarget)
        agent = getVector2D(self.agent)
        vector = normalize(target - agent) * self.agent.maxSpeed
        return vector - self.agent.velocity

    # parecido a seek pero se detiene en el punto
    def arrive(self) -> Vector2D:
        target = getVector2D(self.arriveTarget)
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
    def flee(self) -> Vector2D:
        agent = getVector2D(self.agent)
        target = getVector2D(self.fleeTarget)
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
        circleCenter = Vector2D(self.agent.velocity.x, self.agent.velocity.y)
        circleCenter = normalize(circleCenter)
        circleCenter.x *= WANDER_DIST
        circleCenter.y *= WANDER_DIST
        # calcular fuerza de desplacamiento
        displacement = Vector2D(0, -WANDER_RADIUS)
        # cambiar la direccioncambiando el angulo
        l = displacement.length()
        displacement.x = math.cos(self.wanderAngle) * l
        displacement.y = math.sin(self.wanderAngle) * l
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
    @staticmethod
    def followPath() -> Vector2D:
        pass

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
            wanderForce = self.wander()
            steering.x += wanderForce.x * self.weightWander
            steering.y += wanderForce.y * self.weightWander
        if self.seekEnabled:
            seekForce = self.seek()
            steering.x += seekForce.x * self.weightSeek
            steering.y += seekForce.y * self.weightSeek
        if self.fleeEnabled:
            fleeForce = self.flee()
            steering.x += fleeForce.x * self.weightFlee
            steering.y += fleeForce.y * self.weightFlee
        if self.arriveEnabled:
            arriveForce = self.arrive()
            steering.x += arriveForce.x * self.weightArrive
            steering.y += arriveForce.y * self.weightArrive

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

        # if self.followPathEnabled:
        #     steering += self.followPath() * self.weightFollowPath

        return truncate(steering, self.agent.maxForce)


# //------------------------------ Pursuit ---------------------------------
# //
# //  this behavior creates a force that steers the agent towards the
# //  evader
# //------------------------------------------------------------------------
# Vector2D SteeringBehavior::Pursuit(const Vehicle* evader)
# {
#   //if the evader is ahead and facing the agent then we can just seek
#   //for the evader's current position.
#   Vector2D ToEvader = evader->Pos() - m_pVehicle->Pos();

#   double RelativeHeading = m_pVehicle->Heading().Dot(evader->Heading());

#   if ( (ToEvader.Dot(m_pVehicle->Heading()) > 0) &&
#        (RelativeHeading < -0.95))  //acos(0.95)=18 degs
#   {
#     return Seek(evader->Pos());
#   }

#   //Not considered ahead so we predict where the evader will be.

#   //the lookahead time is propotional to the distance between the evader
#   //and the pursuer; and is inversely proportional to the sum of the
#   //agent's velocities
#   double LookAheadTime = ToEvader.Length() /
#                         (m_pVehicle->MaxSpeed() + evader->Speed());

#   //now seek to the predicted future position of the evader
#   return Seek(evader->Pos() + evader->Velocity() * LookAheadTime);
# }

# //------------------------- Offset Pursuit -------------------------------
# //
# //  Produces a steering force that keeps a vehicle at a specified offset
# //  from a leader vehicle
# //------------------------------------------------------------------------
# Vector2D SteeringBehavior::OffsetPursuit(const Vehicle*  leader,
#                                           const Vector2D offset)
# {
#   //calculate the offset's position in world space
#   Vector2D WorldOffsetPos = PointToWorldSpace(offset,
#                                                   leader->Heading(),
#                                                   leader->Side(),
#                                                   leader->Pos());

#   Vector2D ToOffset = WorldOffsetPos - m_pVehicle->Pos();

#   //the lookahead time is propotional to the distance between the leader
#   //and the pursuer; and is inversely proportional to the sum of both
#   //agent's velocities
#   double LookAheadTime = ToOffset.Length() / 
#                         (m_pVehicle->MaxSpeed() + leader->Speed());
  
#   //now Arrive at the predicted future position of the offset
#   return Arrive(WorldOffsetPos + leader->Velocity() * LookAheadTime, fast);
# }


# //----------------------------- Evade ------------------------------------
# //
# //  similar to pursuit except the agent Flees from the estimated future
# //  position of the pursuer
# //------------------------------------------------------------------------
# Vector2D SteeringBehavior::Evade(const Vehicle* pursuer)
# {
#   /* Not necessary to include the check for facing direction this time */

#   Vector2D ToPursuer = pursuer->Pos() - m_pVehicle->Pos();

#   //uncomment the following two lines to have Evade only consider pursuers
#   //within a 'threat range'
#   const double ThreatRange = 100.0;
#   if (ToPursuer.LengthSq() > ThreatRange * ThreatRange) return Vector2D();

#   //the lookahead time is propotional to the distance between the pursuer
#   //and the pursuer; and is inversely proportional to the sum of the
#   //agents' velocities
#   double LookAheadTime = ToPursuer.Length() /
#                          (m_pVehicle->MaxSpeed() + pursuer->Speed());

#   //now flee away from predicted future position of the pursuer
#   return Flee(pursuer->Pos() + pursuer->Velocity() * LookAheadTime);
# }
