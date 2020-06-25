import pygame

from .Entity import Entity
from .MovingEntity import MovingEntity
from .Vector2D import Vector2D
from .camera.BaseCamera import BaseCamera
from .misc import Colors


class Cell:
    def __init__(self, rect):
        self.members = []
        self.rect = rect


class SpacePartition:
    def __init__(self, width: int, height: int, cellWidth: int, cellHeight: int):
        self.__spaceWidth = width
        self.__spaceHeight = height
        self.__cellWidth = cellWidth
        self.__cellHeight = cellHeight
        self.__numCellsX = (width // cellWidth) + 1
        self.__numCellsY = (height // cellHeight) + 1
        self.__cells = []
        self.__numCells = 0
        offsetX = ((cellWidth - (width % cellWidth)) / 2)
        offsetY = ((cellHeight - (height % cellHeight)) / 2)
        for y in range(0, self.__numCellsY):
            for x in range(0, self.__numCellsX):
                left = x * self.__cellWidth - offsetX
                top = y * self.__cellHeight - offsetY
                self.__cells.append(Cell(
                    pygame.Rect(left, top, self.__cellWidth, self.__cellHeight)
                ))
        self.__numCells = len(self.__cells)

    def clear(self):
        self.emptyCells()
        self.__cells.clear()
        self.__numCells = 0

    def emptyCells(self):
        for cell in self.__cells:
            cell.members.clear()

    @property
    def cellWidth(self):
        return self.__cellWidth

    @property
    def cellHeight(self):
        return self.__cellHeight

    # def calculateNeighbors(self, targetPos: Vector2D, queryRadius: float) -> list:
    def calculateNeighbors(self, queryRect) -> list:
        neighbors = []
        # y si la particion del espacio indexa las entidades entodas las
        # celdas que toca ya no se tendria que arreglar este query rect
        fixedRect = pygame.Rect((0, 0), (self.cellWidth + queryRect.width / 2, self.cellHeight + queryRect.height / 2))
        fixedRect.center = queryRect.center
        for cell in self.__cells:
            if len(cell.members) and fixedRect.colliderect(cell.rect):
                neighbors += cell.members
                cell.tag = True
            else:
                cell.tag = False
        return neighbors

    def registerEntities(self, entities: list):
        for entity in entities:
            self.registerEntity(entity)

    def registerEntity(self, entity: Entity):
        index = self.posToIndex(entity.getPos())
        if 0 <= index < self.__numCells:
            self.__cells[index].members.append(entity)
            entity.cellIndex = index
        else:
            print('❌ No se pudo registrar la entidad', entity)
        return index

    def unregisterEntity(self, entity: Entity):
        index = self.posToIndex(entity.getPos())
        if 0 <= index < self.__numCells:
            if entity in self.__cells[index].members:
                self.__cells[index].members.remove(entity)
        else:
            print('❌ No se pudo desregistrar la entidad', entity)

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

    def updateEntity(self, entity: MovingEntity):
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
                pygame.draw.rect(surface, Colors.RED, camera.apply(cell.rect), 4)
            else:
                pygame.draw.rect(surface, Colors.GRAY, camera.apply(cell.rect), 1)

    def tagAll(self, value):
        for cell in self.__cells:
            cell.tag = value
            for entity in cell.members:
                entity.tag = value

    def tagNeighborhood(self, entity: Entity):
        self.tagAll(False)
        neighbors = self.calculateNeighbors(entity.getCollisionRect())
        if entity in neighbors:
            neighbors.remove(entity)
        for entity in neighbors:
            entity.tag = True
        return neighbors

    def queryObjects(self, queryRect, validation=None) -> list:
        entities = []
        if validation is None:
            def validation(x) -> bool: return True
        neighbors = self.calculateNeighbors(queryRect)
        for entity in neighbors:
            if queryRect.colliderect(entity.getSelectionRect()):
                if validation(entity):
                    entities.append(entity)
        return entities
