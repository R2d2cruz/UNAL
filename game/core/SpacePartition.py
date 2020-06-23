import pygame

from .Entity import Entity
from .Vector2D import Vector2D
from .camera.BaseCamera import BaseCamera


class Cell:
    def __init__(self, rect):
        self.members = []
        self.rect = rect


class SpacePartition:
    def __init__(self, width: int, height: int, cellsX: int, cellsY: int):
        self.__spaceWidth = width
        self.__spaceHeight = height
        self.__numCellsX = cellsX
        self.__numCellsY = cellsY
        self.__cellSizeX = width / cellsX
        self.__cellSizeY = height / cellsY
        self.__cells = []
        self.__numCells = 0
        for y in range(0, self.__numCellsY):
            for x in range(0, self.__numCellsX):
                left = x * self.__cellSizeX
                top = y * self.__cellSizeY
                self.__cells.append(Cell(
                    pygame.Rect(left, top, self.__cellSizeX, self.__cellSizeY)
                ))
        self.__numCells = len(self.__cells)

    def calculateNeighbors(self, targetPos: Vector2D, queryRadius: float) -> list:
        queryRect = pygame.Rect(
            targetPos.x - queryRadius,
            targetPos.y - queryRadius,
            queryRadius * 2,
            queryRadius * 2
        )
        neighbors = []
        for cell in self.__cells:
            if len(cell.members) and queryRect.colliderect(cell.rect):
                neighbors += cell.members
                cell.tag = True
            else:
                cell.tag = False
        return neighbors

    def emptyCells(self):
        for cell in self.__cells:
            cell.members.clear()

    def registerEntities(self, entities: list):
        for entity in entities:
            self.registerEntity(entity)

    def registerEntity(self, entity: Entity):
        index = self.posToIndex(entity.getPos())
        if 0 <= index < self.__numCells:
            self.__cells[index].members.append(entity)
        else:
            print('❌ Entity can not be registered', entity.id, entity.name, entity.getPos())
        return index

    def unregisterEntity(self, entity: Entity):
        index = self.posToIndex(entity.getPos())
        if 0 <= index < self.__numCells:
            if entity in self.__cells[index].members:
                self.__cells[index].members.remove(entity)
        else:
            print('❌ Entity can not be unregistered', entity.id, entity.name, entity.getPos())

    def posToIndex(self, pos: Vector2D) -> int:
        index = int(
            self.__numCellsX * pos.x / self.__spaceWidth
        ) + int(
            self.__numCellsY * pos.y / self.__spaceHeight
        ) * self.__numCellsX
        numCells = len(self.__cells) - 1
        if index > numCells:
            index = numCells
        return index

    def updateEntity(self, entity: Entity):
        if entity.cellIndex is None:
            oldIndex = self.posToIndex(entity.getOldPos())
        else:
            oldIndex = entity.cellIndex
        newIndex = self.posToIndex(entity.getPos())
        if oldIndex != newIndex:
            if 0 <= oldIndex < self.__numCells:
                if entity in self.__cells[oldIndex].members:
                    self.__cells[oldIndex].members.remove(entity)
                    entity.cellIndex = None
                else:
                    print('❌ Entity', entity.id, entity.name, 'not registered')
            if 0 <= newIndex < self.__numCells:
                self.__cells[newIndex].members.append(entity)
                entity.cellIndex = newIndex

    def render(self, surface, camera: BaseCamera):
        for cell in self.__cells:
            if cell.tag:
                color = (255, 0, 0)
                pygame.draw.rect(surface, color, camera.apply(cell.rect), 4)
            else:
                color = (0, 0, 0)
                pygame.draw.rect(surface, color, camera.apply(cell.rect), 1)

    def tagAll(self, value):
        for cell in self.__cells:
            cell.tag = value
            for entity in cell.members:
                entity.tag = value

    def tagNeighborhood(self, entity: Entity, queryRadius: float):
        self.tagAll(False)
        neighbors = self.calculateNeighbors(entity.getPos(), queryRadius)
        if entity in neighbors:
            neighbors.remove(entity)
        for entity in neighbors:
            entity.tag = True
        return neighbors
