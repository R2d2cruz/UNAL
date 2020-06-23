from .Entity import Entity
from .EntityManager import entityManager
from .MovingEntity import MovingEntity
from .SpacePartition import SpacePartition
from .Vector2D import Vector2D


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
    def inBoundaries(rect, entity: Entity):
        coll = entity.getCollisionRect()
        if coll.left < rect.left or coll.right > rect.right:
            return False
        if coll.top < rect.top or coll.bottom > rect.bottom:
            return False
        return True

    @staticmethod
    def update(cellSpace: SpacePartition, worldRect):
        for entityA in entityManager.movingEntities:
            entityA.tag = False
            if not _CollisionManager.inBoundaries(worldRect, entityA):
                # side = sideColl(entityA, worldRect)
                side = [True, True]
                entityA.stop(side[0], side[1])
            else:
                neighbors = cellSpace.calculateNeighbors(entityA.getPos(), 75)
                for entityB in neighbors:
                    if entityA != entityB:
                        if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                            entityA.tag = True
                            entityB.tag = True
                            if entityB.flag == "item":
                                entityB.effect(entityA)
                            elif entityA.flag == "item":
                                entityA.effect(entityB)
                            else:
                                side = sideColl(entityA, entityB)
                                # side = [True, True]
                                entityA.stop(side[0], side[1])
                        else:
                            entityB.tag = False

    @staticmethod
    def checkCollition(rect, cellSpace) -> bool:
        neighbors = cellSpace.calculateNeighbors(Vector2D(rect.x, rect.y), 75)
        for neighbor in neighbors:
            if rect.colliderect(neighbor.getCollisionRect()):
                return True
        return False


collisionManager = _CollisionManager()
