import pygame

from .Entity import Entity
from .MovingEntity import MovingEntity


class _EntityManager:
    def __init__(self):
        self.__entityMap = {}
        self.movingEntities = set()
        self.entities = set()
        self.walls = set()

    @property
    def allEntities(self):
        return self.__entityMap.values()

    def registerEntities(self, entities: list):
        for entity in entities:
            self.registerEntity(entity)

    def registerEntity(self, entity):
        if entity is not None:
            if isinstance(entity, MovingEntity):
                self.__entityMap[entity.id] = entity
                self.movingEntities.add(entity)
            elif isinstance(entity, Entity):
                self.__entityMap[entity.id] = entity
                self.entities.add(entity)
            elif isinstance(entity, pygame.Rect):
                self.walls.add(entity)

    def unregisterEntity(self, entity: Entity):
        del self.__entityMap[entity.id]

    def getEntityById(self, _id: int):
        return self.__entityMap.get(_id)

    def removeEntityById(self, _id: int):
        if self.__entityMap.get(_id) is not None:
            self.__entityMap.pop(_id)


entityManager = _EntityManager()
