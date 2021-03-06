import pygame

from .v2D import Vector2D


class Path:
    def __init__(self):
        self.__currentPointIndex = 0
        self.__finished = False
        self.points = []

    def isFinished(self):
        return self.__finished

    def setNextPoint(self):
        if self.__currentPointIndex < len(self.points) - 1:
            self.__currentPointIndex += 1
        else:
            self.__finished = True

    def getCurrentWayPoint(self) -> Vector2D:
        point = self.points[self.__currentPointIndex]
        return Vector2D(point[0], point[1])

    def render(self, surface, camera):
        nodeColor = (64, 64, 64)
        currentColor = (255, 0, 0)
        prevPoint = None
        for point in self.points:
            pygame.draw.circle(surface, nodeColor, camera.apply(point), 5, 3)
            if prevPoint is not None:
                pygame.draw.line(surface, nodeColor, camera.apply(point), camera.apply(prevPoint), 2)
            prevPoint = point
        point = self.points[self.__currentPointIndex]
        if point is not None:
            pygame.draw.circle(surface, currentColor, camera.apply(point), 5, 3)

    # def renderNode(self, surface, camera, cords, color):
    #     cords[0] = int(cords[0]) * self.tileWidth + self.tileWidth / 2 
    #     cords[1] = int(cords[1]) * self.tileHeight + self.tileHeight / 2 
    #     pygame.draw.circle(surface, color, camera.apply(cords), 5, 3)

    # def renderArc(self, surface, camera, cords, arc, color):
    #     cordsM = arc.split(',')
    #     cordsM[0] = int(cordsM[0]) * self.tileWidth + self.tileWidth / 2 
    #     cordsM[1] = int(cordsM[1]) * self.tileHeight + self.tileHeight / 2 
    #     pygame.draw.line(surface, color, camera.apply(cords), camera.apply(cordsM), 2)
