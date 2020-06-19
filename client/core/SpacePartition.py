import pygame


from .Vector2D import Vector2D
from .Entity import Entity
from .camera.BaseCamera import BaseCamera

class Cell:
    def __init__(self, rect):
        self.__members = []
        self.rect = rect

class SpacePartition:
    def __init__(self, width: int, height: int, cellsX: int, cellsY: int):
        self.__spaceWidth = width
        self.__spaceHeight = height
        self.__numCellsX = cellsX
        self.__numCellsY = cellsY
        self.__cellSizeX = width  / cellsX
        self.__cellSizeY = height / cellsY
        self.__cells = []
        for y in range(0, self.__numCellsY):
            for x in range(0, self.__numCellsX):
                left  = x * self.__cellSizeX
                top = y * self.__cellSizeY
                self.__cells.append(Cell(
                    pygame.Rect(left, top, left + self.__cellSizeX, top + self.__cellSizeY)
                ))

    def calculateNeighbors(self, targetPos: Vector2D, queryRadius: float):
        queryRect = pygame.Rect(
            targetPos.x - queryRadius,
            targetPos.y - queryRadius,
            targetPos.x + queryRadius,
            targetPos.y + queryRadius
        )
        neighbors = []
        for cell in self.__cells:
            if len(cell.members) and cell.rect.colliderect(queryRect):
                neighbors += cell.members
        return neighbors

    def emptyCells(self):
        for cell in self.__cells:
            cell.members.clear()

    def addEntity(self, entity: Entity):
        index = self.posToIndex(entity.getPos())
        self.__cells[index].members.append(entity)
        
    def positionToIndex(self, pos: Vector2D) -> int:
        index = int(
                    self.__numCellsX * pos.x / self.__spaceWidth
                ) + int(
                    self.__numCellsY * pos.y / self.__spaceHeight
                ) * self.__numCellsX
        numCells = len(self.__cells) - 1
        if index > numCells:
            index = numCells
        return index

    def updateEntity(self, entity: Entity, oldPos: Vector2D):
        oldIndex = self.posToIndex(oldPos)
        newIndex = self.posToIndex(entity.getPos())
        if oldIndex == newIndex:
            return

        self.__cells[oldIndex].members.remove(entity)
        self.__cells[newIndex].members.append(entity)

    def render(self, screen, camera: BaseCamera):
        for cell in self.__cells:
            pygame.draw.rect(screen, (0, 0, 255), camera.apply(cell.rect), 1)