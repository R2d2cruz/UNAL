import pygame

from .Entity import Entity
from .EntityManager import entityManager
from .MovingEntity import MovingEntity
from .SpacePartition import SpacePartition


def sideColl(bodyA: MovingEntity, bodyB: MovingEntity):
    contact = [False, False]
    minBody, maxBody = (bodyA, bodyB) if bodyA.getCollisionRect().x < bodyB.getCollisionRect().x else (bodyB, bodyA)
    minBodyColl = minBody.getCollisionRect()
    maxBodyColl = maxBody.getCollisionRect()
    if minBodyColl.x + minBodyColl.w >= maxBodyColl.x:
        contact[0] = minBody.getOldCollisionRect().x + minBodyColl.w <= maxBodyColl.x or \
                     maxBody.getOldCollisionRect().x >= minBodyColl.x + minBodyColl.w

    minBody, maxBody = (bodyA, bodyB) if bodyA.getCollisionRect().y < bodyB.getCollisionRect().y else (bodyB, bodyA)
    minBodyColl = minBody.getCollisionRect()
    maxBodyColl = maxBody.getCollisionRect()

    if minBodyColl.y + minBodyColl.h >= maxBodyColl.y:
        contact[1] = minBody.getOldCollisionRect().y + minBodyColl.h <= maxBodyColl.y or \
                     maxBody.getOldCollisionRect().y >= minBodyColl.y + minBodyColl.h

    return contact


class _CollisionManager:
    @staticmethod
    def inBoundaries(bounds, coll):
        if coll.left < bounds.left or coll.right > bounds.right:
            return False
        if coll.top < bounds.top or coll.bottom > bounds.bottom:
            return False
        return True

    @staticmethod
    def update(cellSpace: SpacePartition, worldRect):
        for entityA in entityManager.movingEntities:
            entityA.tag = False
            if not _CollisionManager.inBoundaries(worldRect, entityA.getCollisionRect()):
                # side = sideColl(entityA, worldRect)
                side = [True, True]
                entityA.stop(side[0], side[1])
            else:
                queryRect = pygame.Rect(0, 0, cellSpace.cellWidth * 1.2, cellSpace.cellHeight * 1.2)
                queryRect.center = entityA.getCollisionRect().center
                neighbors = cellSpace.calculateNeighbors(queryRect)
                for entityB in neighbors:
                    if entityA != entityB:
                        if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                            if entityB.type == "item":
                                entityB.effect(entityA)
                            elif entityA.type == "item":
                                entityA.effect(entityB)
                            else:
                                # side = sideColl(entityA, entityB)
                                side = [True, True]
                                entityA.stop(side[0], side[1])

    @staticmethod
    def checkCollition(queryRect, cellSpace, worldRect) -> bool:
        if _CollisionManager.inBoundaries(worldRect, queryRect):
            neighbors = cellSpace.calculateNeighbors(queryRect)
            for neighbor in neighbors:
                if queryRect.colliderect(neighbor.getCollisionRect()):
                    return True
        return False

    @staticmethod
    def queryObjects(queryRect, cellSpace, validation=None) -> list:
        entities = []
        if validation is None:
            def validation(x) -> bool: return True
        rect = queryRect.copy()
        rect.width = max(queryRect.width, cellSpace.cellWidth * 1.2)
        rect.height = max(queryRect.height, cellSpace.cellHeight * 1.2)
        rect.center = queryRect.center
        neighbors = cellSpace.calculateNeighbors(rect)
        for entity in neighbors:
            if queryRect.colliderect(entity.getSelectionRect()):
                if validation(entity):
                    entities.append(entity)
        return entities

    def getCloseNeighbors(self, entity: Entity, cellSpace, validation=None) -> list:
        entities = self.queryObjects(entity.getCollisionRect(), cellSpace, validation=validation)
        return [x.getMe for x in entities]


collisionManager = _CollisionManager()
