import pygame

from .Entity import Entity
from .MovingEntity import MovingEntity


class _EntityManager:
    def __init__(self):
        self.__entityMap = {}
        self.movingEntities = set()
        self.entities = set()
        self.walls = set()
        self.other = {}
        self.__worldId = None

    @property
    def allEntities(self):
        return self.__entityMap.values()

    @property
    def worldId(self):
        return self.__worldId

    @worldId.setter
    def worldId(self, _id):
        self.__worldId = _id

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
                # self.__entityMap[entity.id] = entity
                self.walls.add(entity)
            else:
                self.other[entity.id] = entity

    def unregisterEntity(self, entity: Entity):
        del self.__entityMap[entity.id]
        if isinstance(entity, MovingEntity):
            self.movingEntities.remove(entity)
        elif isinstance(entity, Entity):
            self.entities.remove(entity)
        elif isinstance(entity, pygame.Rect):
            self.walls.remove(entity)

    def getEntityById(self, _id: int):
        entity = self.__entityMap.get(_id)
        return entity if entity is not None else self.other.get(_id)


entityManager = _EntityManager()
