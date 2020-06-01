import pygame 
from core.Vector2D import Vector2D


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

    def render(self, screen, camera):
        color = (0, 0, 255)
        prevPoint = None
        for point in self.points:
            pygame.draw.circle(screen, color, camera.apply(point), 5, 3)
            if prevPoint is not None:
                pygame.draw.line(screen, color, camera.apply(point), camera.apply(prevPoint), 2)
            prevPoint = point

    # def renderNode(self, screen, camera, cords, color):
    #     cords[0] = int(cords[0]) * self.tileWidth + self.tileWidth / 2 
    #     cords[1] = int(cords[1]) * self.tileHeight + self.tileHeight / 2 
    #     pygame.draw.circle(screen, color, camera.apply(cords), 5, 3)

    # def renderArc(self, screen, camera, cords, arc, color):
    #     cordsM = arc.split(',')
    #     cordsM[0] = int(cordsM[0]) * self.tileWidth + self.tileWidth / 2 
    #     cordsM[1] = int(cordsM[1]) * self.tileHeight + self.tileHeight / 2 
    #     pygame.draw.line(screen, color, camera.apply(cords), camera.apply(cordsM), 2)
