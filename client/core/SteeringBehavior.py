import math
import random
from core.Vector2D import *


# el radio limite para wander
WANDER_RADIUS = 1.2
# distancia de proyeccion del circulo de wnader frente a la entidad
WANDER_DIST = 2.0
# maximo desplazamiento en el circulo por segundo
WANDER_JITTER_PER_SECOND = 80.0

def randomClamped():
    return random.random() - random.random()

class SteeringBehavior:
    def __init__(self, agent):
        theta = random.random() * math.pi * 2
        self.agent = agent
        self.wanderTarget = Vector2D(WANDER_RADIUS * math.cos(theta), WANDER_RADIUS * math.sin(theta))
        self.wanderJitter = WANDER_JITTER_PER_SECOND
        pass

    # retorna un vector para mover la entidad hacia la posicion dada
    @staticmethod
    def seek(targetPos: Vector2D) -> Vector2D:
        pass

    # retorna un vector para mover la entidad lejos de la posicion dada
    @staticmethod
    def flee(targetPos: Vector2D) -> Vector2D:
        pass

    # parecido a seek pero se detiene en el punto
    @staticmethod
    def arrive(target: Vector2D, deceleration: float) -> Vector2D:
        pass

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
    def wander(self, deltatime) -> Vector2D:
        jitter = self.wanderJitter * deltatime
        self.wanderTarget += Vector2D(randomClamped() * jitter, randomClamped() * jitter)
        self.wanderTarget = normalize(self.wanderTarget)
        self.wanderTarget.x *= WANDER_RADIUS
        self.wanderTarget.y *= WANDER_RADIUS

        target = Vector2D(self.wanderTarget.x + WANDER_DIST, self.wanderTarget.y + 0)

        # //project the target into world space
        # Vector2D Target = PointToWorldSpace(target,
        #                                     m_pVehicle->Heading(),
        #                                     m_pVehicle->Side(), 
        #                                     m_pVehicle->Pos());

        # ir hacia el target
        return Vector2D(target - self.agent.x, target.y - self.agent.y); 


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
        return Vector2D()