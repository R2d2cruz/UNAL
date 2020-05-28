class SteeringBehavior:
    def __init__(self):
        pass

    # retorna un vector para mover la entidad hacia la posicion dada
    @staticmethod
    def seek(targetPos):
        pass

    # retorna un vector para mover la entidad lejos de la posicion dada
    @staticmethod
    def flee(targetPos):
        pass

    # parecido a seek pero se detiene en el punto
    @staticmethod
    def arrive(target, deceleration):
        pass

    # predice donde estara la entidad y retorna el seek hacia ese punto
    @staticmethod
    def pursuit(entity):
        pass

    # persigue  anteniendo una distancia
    @staticmethod
    def offsetPursuit(entity, offset):
        pass

    # evadir una entidad
    @staticmethod
    def evade(entity):
        pass

    # el wander que tanto necesitas hijo
    @staticmethod
    def wander():
        pass

    # evadir varios obstaculos
    @staticmethod
    def obstacleAvoidance(obstacles: list):
        pass

    # evadir paredes
    @staticmethod
    def wallAvoidance(walls):
        pass

    # seguir una ruta
    @staticmethod
    def followPath():
        pass

    # interponerse entre dos entidades
    @staticmethod
    def interpose(entityA, entityB):
        pass

    # se oculta de otra entidad tras los obstculos dados
    @staticmethod
    def hide(hunter, obstacles):
        pass

    # la suma de todas las fuerzas que operan sobre la entidad
    def calculate(self):
        return (0, 0)