from game.core import Vector2D
from game.core.Character import Character
from game.core.Hermes import hermes


class CharacterWrapper:
    def __init__(self, entity: Character, position: Vector2D):
        self._entity = entity
        self._steeringOn = False
        self._entity.setPos(position.x, position.y)
        self._path = None

    def sendMessage(self, receiver: int, msg: str, extraInfo: dict, delay: float = 0):
        hermes.messageDispatch(delay, self._entity.id, receiver, msg, extraInfo)

    def onInit(self, name: str):
        self._entity.setName(name)

    def setPath(self, path: classmethod):
        self._path = path

    def goDirection(self, direction: Vector2D):
        if self._steeringOn:
            self.setSteeringOff()
        self._entity.velocity = direction

    def goDirectionWithPoint(self, point: Vector2D):
        if self._steeringOn:
            self.setSteeringOff()
        self._entity.steering.arriveEnabled = True
        self._entity.steering.arriveTarget = point
        self._steeringOn = True

    def goAroundAnAPoint(self, point: Vector2D):
        if self._steeringOn:
            self.setSteeringOff()
        self._entity.steering.seekEnabled = True
        self._entity.steering.seekTarget = point
        self._steeringOn = True

    def goPosition(self, position: Vector2D):
        if self._steeringOn:
            self.setSteeringOff()
        self._entity.steering.followPathEnabled = True
        self._entity.steering.followPathTarget = self._path(self._path(self._entity, position))
        self._steeringOn = True

    def wander(self, weightWander: float = 0.5):
        self._entity.steering.wanderEnabled = True
        self._entity.steering.weightWander = weightWander
        self._steeringOn = True

    def setSteeringOff(self):
        self._entity.steering.seekEnabled = False
        self._entity.steering.seekTarget = None
        self._entity.steering.arriveEnabled = False
        self._entity.steering.arriveTarget = None
        self._entity.steering.followPathEnabled = False
        self._entity.steering.followPathTarget = None
        self._entity.steering.wanderEnabled = False
