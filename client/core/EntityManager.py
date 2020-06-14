from core.Entity import Entity
from core.Telegram import Telegram
import core.Hermes as Hermes

__entities = {}
__entityMap = None
__deltaTime = 0


def init():
    global __entities
    global __entityMap
    __entityMap = None
    __entities = {}


def entityMap():
    return __entityMap


def setEntityMap(_entityMap):
    global __entityMap
    __entityMap = _entityMap


def discharge(pReceiver: int, msg: Telegram):
    pass


def registerEntities(entities: list):
    for entity in entities:
        registerEntity(entity)


def registerEntity(entity: Entity):
    global __entities
    __entities[entity.id] = entity


def getEntityById(_id: int):
    return __entities.get(_id)


def removeEntityById(_id: int):
    global __entities
    if __entities.get(_id) is not None:
        __entities.pop(_id)
