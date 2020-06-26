import pygame

from . import World, SimpleCamera, collisionManager


class SelectionBox:
    def __init__(self):
        self.__pointA = None
        self.__pointB = None
        self.__entities = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.valid = False
        self.visible = False

    @property
    def entities(self):
        return self.__entities

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setPointA(self, point):
        self.clear()
        if point is not None:
            self.__pointA = point
            self.visible = True

    def setPointB(self, point):
        if point is not None:
            self.visible = True
            self.x = min(self.__pointA[0], point[0])
            self.y = min(self.__pointA[1], point[1])
            self.width = max(1, abs(self.__pointA[0] - point[0]))
            self.height = max(1, abs(self.__pointA[1] - point[1]))
            if self.width > 0 and self.height > 0:
                self.valid = True

    def clear(self):
        self.__pointA = None
        self.__pointB = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.valid = False
        self.visible = False
        for entity in self.__entities:
            entity.selected = False
        self.__entities.clear()

    def render(self, surface):
        if self.visible:
            if self.valid:
                box = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                box.fill((0, 255, 0, 128))
                pygame.draw.rect(box, pygame.Color(0, 255, 0, 255), (0, 0, self.width, self.height), 1)
                surface.blit(box, (self.x, self.y))
            else:
                pygame.draw.circle(surface, (0, 255, 0), self.__pointA, 4, 2)

    def getSelectionPoint(self, point, world: World, camera: SimpleCamera):
        point = camera.unapply(point)
        point.x -= world.view.x
        point.y -= world.view.y
        return point

    def selectEntities(self, world: World, camera: SimpleCamera):
        rect = self.getSelectionPoint(self.getRect(), world, camera)
        self.visible = False
        for entity in self.__entities:
            entity.selected = False
        self.__entities = world.cellSpace.queryObjects(rect)
        for entity in self.__entities:
            entity.selected = True
