from .SpacePartition import SpacePartition
from .Vector2D import Vector2D
from .Entity import Entity
from .MovingEntity import MovingEntity


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
    def __init__(self):
        self.movingEntities = set()
        self.entities = set()
        self.walls = set()

    def registerEntities(self, entities: list):
        for entity in entities:
            self.registerEntity(entity)

    def registerEntity(self, entity: Entity):
        self.entities.add(entity)

    def registerMovingEntities(self, entities: list):
        for entity in entities:
            self.registerMovingEntity(entity)

    def registerMovingEntity(self, entity: MovingEntity):
        self.movingEntities.add(entity)

    def update(self, cellSpace: SpacePartition):
        for entityA in self.movingEntities:
            entityA.tag = False
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
                            #side = [True, True]
                            entityA.stop(side[0], side[1])
                    else:
                        entityB.tag = False

    def checkCollistion(self, rect, cellSpace) -> bool:
        neighbors = cellSpace.calculateNeighbors(Vector2D(rect.x, rect.y), 75)
        for neighbor in neighbors:
            if rect.colliderect(neighbor.getCollisionRect()):
                return True
        return False


collisionManager = _CollisionManager()
