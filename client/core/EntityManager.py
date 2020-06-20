from .Entity import Entity
from .Telegram import Telegram


class _EntityManager:
    def __init__(self):
        self.__entities = {}
        self.__entityMap = None
        self.__deltaTime = 0

    def discharge(self, pReceiver: int, msg: Telegram):
        pass

    def registerEntities(self, entities: list):
        for entity in entities:
            self.registerEntity(entity)

    def registerEntity(self, entity: Entity):
        self.__entities[entity.id] = entity

    def unregisterEntity(self, entity: Entity):
        del self.__entities[entity.id]

    def getEntityById(self, _id: int):
        return self.__entities.get(_id)

    def removeEntityById(self, _id: int):
        if self.__entities.get(_id) is not None:
            self.__entities.pop(_id)


entityManager = _EntityManager()
