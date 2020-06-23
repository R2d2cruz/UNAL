from random import random, choice

import pygame

from . import SpacePartition, TiledMap, entityManager, collisionManager, Entity, MovingEntity, Path, Graph, Character, Vector2D


class World:
    def __init__(self, tiledMap: TiledMap, view: pygame.Rect):
        self.rect = pygame.Rect(0, 0, tiledMap.width, tiledMap.height)
        self.view = view
        self.player = None
        self.map = tiledMap
        self.graph = Graph()
        self.graph.nodes = Graph.getGraph(tiledMap, True)
        self.cellSpace = SpacePartition(self.rect.w, self.rect.h, int(self.rect.w / 100), int(self.rect.h / 100))
        self.worldSurface = pygame.Surface((view.width, view.height))
        self.cellSpace.registerEntities(tiledMap.getWalls())
        # entityManager.registerEntities(tiledMap.objects)
        # collisionManager.registerEntities(tiledMap.getWalls())  # las paredes no deberian ser objetos... o si?

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
                entity.script.onUpdate(entity)
            entity.update(deltaTime)
            if isinstance(entity, MovingEntity):
                self.cellSpace.updateEntity(entity)

        collisionManager.update(self.cellSpace, self.rect)

    def render(self, surface, camera):
        self.worldSurface.fill((0, 0, 0))
        self.map.render(self.worldSurface, camera)
        for entity in entityManager.allEntities:
            entity.render(self.worldSurface, camera)
        # self.graph.render(self.worldSurface, camera)
        surface.blit(self.worldSurface, self.view)

    def getValidRandomPos(self, rect: pygame.Rect):
        while True:
            rect.x = int(random() * self.rect.w)
            rect.y = int(random() * self.rect.h)
            if not collisionManager.checkCollition(rect, self.cellSpace):
                return rect

    def locateInValidRandomPos(self, entity: Entity):
        pos = self.getValidRandomPos(entity.getCollisionRect())
        entity.setPos(pos.x, pos.y)

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
