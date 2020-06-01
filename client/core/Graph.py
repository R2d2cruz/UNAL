import pygame
from collections import deque
from random import choice

class Graph:
    def __init__(self):
        self.nodes = {}
        self.tileWidth = 32
        self.tileHeight = 32

    # def render(self, screen, camera):
    #     for n in self.nodes:
    #         cords = n.split(',')
    #         self.renderNode(screen, camera, cords, (255, 225, 0))
    #         for arc in self.nodes[n]:
    #             self.renderArc(screen, camera, cords, arc, (255, 255, 0))

    # def renderPath(self, screen, camera, path):
    #     if path is not None:
    #         prevNode = None
    #         for node in path:
    #             cords = node.split(',')
    #             self.renderNode(screen, camera, cords, (255, 0, 0))
    #             if prevNode is not None:
    #                 self.renderArc(screen, camera, cords, prevNode, (255, 0, 0))
    #             prevNode = node

    # def renderNode(self, screen, camera, cords, color):
    #     cords[0] = int(cords[0]) * self.tileWidth + self.tileWidth / 2 
    #     cords[1] = int(cords[1]) * self.tileHeight + self.tileHeight / 2 
    #     pygame.draw.circle(screen, color, camera.apply(cords), 5, 3)

    # def renderArc(self, screen, camera, cords, arc, color):
    #     cordsM = arc.split(',')
    #     cordsM[0] = int(cordsM[0]) * self.tileWidth + self.tileWidth / 2 
    #     cordsM[1] = int(cordsM[1]) * self.tileHeight + self.tileHeight / 2 
    #     pygame.draw.line(screen, color, camera.apply(cords), camera.apply(cordsM), 2)

    def findShortestPath(self, start: str, end: str) -> list:
        dist = {start: [start]}
        if start not in self.nodes.keys():
            return []
        if end not in self.nodes.keys():
            return dist
        q = deque([start])
        while len(q):
            at = q.popleft()
            for nextNode in self.nodes[at]:
                if nextNode not in dist:
                    dist[nextNode] = dist[at] + [nextNode]
                    q.append(nextNode)
        return dist.get(end)

    def findShortestPath2(self, start: str, end: str) -> list:
        dist = {start: [start]}
        if start not in self.nodes.keys():
            return []
        if end not in self.nodes.keys():
            return dist
        q = deque([start])
        while len(q):
            at = q.popleft()
            for nextNode in self.nodes[at]:
                if nextNode not in dist:
                    dist[nextNode] = dist[at] + [nextNode]
                    q.append(nextNode)
        return dist.get(end)

    def randomPath(self, start=None, end=None) -> list:
        self.nodeStart = choice(list(self.nodes.keys())) if start is None else start
        self.nodeEnd = choice(list(self.nodes.keys())) if end is None else end
        return self.findShortestPath(self.nodeStart, self.nodeEnd)