from core.Entity import Entity
from core.MovingEntity import MovingEntity

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
        # quitar marcas
        for entity in self.movingEntities:
            entity.isInCollision = False

        for entityA in self.movingEntities:
            # contra items fijos
            for entityB in self.entities:
                if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                    #entityA.isInCollision = True # solo se marca 1, el otro se marca en la otra ronda
                    entityA.stop()
            # contra todos, esto se puede optimizar para no repetir validaciones
            for entityB in self.movingEntities:
                if entityA != entityB:
                    if entityA.getCollisionRect().colliderect(entityB.getCollisionRect()):
                        # entityA.isInCollision = True # solo se marca 1, el otro se marca en la otra ronda
                        entityA.stop()

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