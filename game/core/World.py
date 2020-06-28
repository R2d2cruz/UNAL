from random import random, choice

import pygame

from . import MovingEntity, Character, collisionManager, Entity, entityManager, Graph, Path, SpacePartition, TiledMap, \
    Vector2D
from .Telegram import Telegram


class World:
    def __init__(self, tiledMap: TiledMap, view: pygame.Rect):
        self.rect = pygame.Rect(0, 0, tiledMap.width, tiledMap.height)
        self.view = view
        self.player = None
        self.map = tiledMap
        self.graph = Graph()
        self.graph.nodes = Graph.getGraph(tiledMap, True)
        self.script = None
        self.cellSpace = SpacePartition(self.rect.w, self.rect.h, 100, 100)
        self.worldSurface = pygame.Surface((view.width, view.height))

        self.cellSpace.registerEntities(tiledMap.getWalls())
        # entityManager.registerEntities(tiledMap.getWalls())
        self.cellSpace.registerEntities(tiledMap.objects)
        entityManager.registerEntities(tiledMap.objects)
        entityManager.registerEntity(self)
        entityManager.worldId = self.id

    def clear(self):
        # self.map.clear()
        # self.graph.clear()
        self.graph.nodes.clear()
        self.cellSpace.clear()
        entityManager.clear()

    @property
    def id(self):
        return id(self)

    def createBook(self, name: str, position: Vector2D, data: dict, rect: tuple = (12, 12, 32, 40)) -> Entity:
        pass

    def addEntity(self, entity, isSolid: bool = True):
        if isSolid:
            self.cellSpace.registerEntity(entity)
        entityManager.registerEntity(entity)

    def removeEntity(self, entity):
        collisionManager.unregisterMovingEntity(entity)
        entityManager.unregisterEntity(entity)
        self.cellSpace.unregisterEntity(entity)

    def update(self, deltaTime: float):
        for entity in entityManager.allEntities:
            if entity.script is not None:
                entity.wrapper.setPath(self.followPositionPath)
                entity.script.onUpdate(entity.wrapper, collisionManager.getCloseNeighbors(entity, self.cellSpace))
            entity.update(deltaTime)
            if issubclass(type(entity), MovingEntity):
                self.cellSpace.updateEntity(entity)

        collisionManager.update(self.cellSpace, self.rect)

    def render(self, surface, camera):
        self.worldSurface.fill((0, 0, 0))
        self.map.render(self.worldSurface, camera)
        for entity in entityManager.allEntities:
            entity.render(self.worldSurface, camera)
        # self.graph.render(self.worldSurface, camera)
        # self.cellSpace.render(self.worldSurface, camera)
        surface.blit(self.worldSurface, self.view)

    def getValidRandomPos(self, entity: Entity) -> Vector2D:
        # se necesita el entity porque el collision rect se calcula diferente segun el tipo
        posX = entity.x
        posY = entity.y
        while True:
            entity.setPos(int(random() * self.rect.w), int(random() * self.rect.h))
            if not collisionManager.checkCollition(entity.getCollisionRect(), self.cellSpace, self.rect):
                newPos = Vector2D(entity.x, entity.y)
                entity.setPos(posX, posY)
                return newPos

    def locateInValidRandomPos(self, entity: Entity):
        newPos = self.getValidRandomPos(entity)
        entity.setPos(newPos.x, newPos.y)
        if isinstance(entity, MovingEntity):
            self.cellSpace.updateEntity(entity)

    def followRandomPath(self, entity: Character):
        nodeEnd = choice(list(self.graph.nodes.keys()))
        self.followPath(entity, nodeEnd)

    def followPath(self, entity: Character, endNode: str):
        node = self.map.pointToCell(entity.x, entity.y)
        graphPath = self.graph.path(node, endNode)
        realPath = Path()
        if len(graphPath) > 0:
            for node in graphPath:
                realPath.points.append(self.map.cellToPoint(node))
            entity.steering.followPathEnabled = True
            entity.steering.followPathTarget = realPath

    def followPositionPath(self, entity: Character, position: Vector2D):
        node = self.map.pointToCell(position.x, position.y)
        self.followPath(entity, node)

    def onMessage(self, telegram: Telegram):
        if telegram.message == 'deleteMe':
            entity = entityManager.getEntityById(telegram.sender)
            if entity is not None:  # esto no deberia ocurrir
                self.cellSpace.unregisterEntity(entity)
                entityManager.unregisterEntity(entity)
            else:
                print('Se intentó eliminar entidad inexistente ', telegram.sender)
        elif telegram.message == 'createBook':
            position = telegram.extraInfo.get('position')
            self.addEntity(self.createBook(telegram.extraInfo.get('tittle'), Vector2D(position[0], position[1]),
                                           telegram.extraInfo.get('book')))
