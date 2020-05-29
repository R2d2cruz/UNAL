from core.Vector2D import Vector2D

class SteeringBehavior:
    def __init__(self):
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
    @staticmethod
    def wander() -> Vector2D:
        pass

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