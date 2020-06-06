from core.Entity import Entity


class EntityManager:

    def __init__(self):
        self.__entityMap = None
        self.__entities = {}

    @property
    def entityMap(self):
        return self.__entityMap

    @entityMap.setter
    def entityMap(self, entityMap):
        self.__entityMap = entityMap

    def discharge(self, pReceiver, msg):
        pass

    def registerEntity(self, entities: list):
        for entity in entities:
            if entity.__class__ is Entity:
                self.__entities[entity.id] = entity

    def getEntityById(self, _id: int):
        return self.__entities[_id]

    def removeEntityById(self, _id):
        if self.__entities.get(_id) is not None:
            self.__entities.pop(_id)
