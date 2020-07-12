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
            # entityA.tag = False
            if not _CollisionManager.inBoundaries(worldRect, entityA.getCollisionRect()):
                # side = sideColl(entityA, worldRect)
                side = [True, True]
                entityA.stop(side[0], side[1])
            else:
                neighbors = cellSpace.calculateNeighbors(entityA.getCollisionRect())
                for entityB in neighbors:
                    if entityA != entityB and entityB.tangible:
                        if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                            if entityB.type == "item":
                                entityB.effect(entityA)
                            elif entityA.type == "item":
                                entityA.effect(entityB)
                            else:
                                side = sideColl(entityA, entityB)
                                # side = [True, True]
                                entityA.stop(side[0], side[1])
                                entityA.onCollision(entityB)
                                entityB.onCollision(entityA)

    @staticmethod
    def checkCollition(queryRect, cellSpace, worldRect) -> bool:
        if not _CollisionManager.inBoundaries(worldRect, queryRect):
            return True
        neighbors = cellSpace.calculateNeighbors(queryRect)
        for neighbor in neighbors:
            if queryRect.colliderect(neighbor.getCollisionRect()):
                return True
        return False


collisionManager = _CollisionManager()
