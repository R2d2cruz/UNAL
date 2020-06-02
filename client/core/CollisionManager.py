from core.Entity import Entity
from core.MovingEntity import MovingEntity


def coll(pos1, gross1, pos2, gross2):
    pass


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


class CollisionManager:
    def __init__(self):
        self.movingEntities = set()
        self.entities = set()
        self.walls = set()

    def registerEntity(self, entity: Entity):
        self.entities.add(entity)

    def registerMovingEntity(self, entity: MovingEntity):
        self.movingEntities.add(entity)

    def update(self):
        removeEntities = []
        # quitar marcas
        for entity in self.movingEntities:
            entity.isInCollision = False

        for entityA in self.movingEntities:
            # contra items fijos
            for entityB in self.entities:
                if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                    # entityA.isInCollision = True # solo se marca 1, el otro se marca en la otra ronda
                    if entityB.flag == "item":
                        if entityB.effect(entityA):
                            removeEntities.append(entityB)
                    elif entityA.flag == "item":
                        if entityA.effect(entityB):
                            removeEntities.append(entityA)
                    else:
                        side = sideColl(entityA, entityB)

                        entityA.stop(side[0], side[1])

            # contra todos, esto se puede optimizar para no repetir validaciones
            for entityB in self.movingEntities:
                if entityA != entityB:
                    if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                        # entityA.isInCollision = True # solo se marca 1, el otro se marca en la otra ronda
                        side = sideColl(entityA, entityB)

                        entityA.stop(side[0], side[1])

            for entity in removeEntities:
                self.entities.remove(entity)

    def checkCollistion(self, rect) -> bool:
        for entity in self.entities:
            if rect.colliderect(entity.getCollisionRect()):
                return True
        # contra todos, esto se puede optimizar para no repetir validaciones
        for entity in self.movingEntities:
            if rect.colliderect(entity.getCollisionRect()):
                return True
        return False


collisionManager = CollisionManager()
