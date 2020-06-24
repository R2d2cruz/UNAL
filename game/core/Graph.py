from collections import deque
from random import choice

import pygame

from .TiledMap import TiledMap


class Graph:
    def __init__(self):
        self.nodes = {}
        self.tileWidth = 32
        self.tileHeight = 32

    def render(self, surface, camera):
        for n in self.nodes:
            cords = n.split(',')
            self.renderNode(surface, camera, cords, (255, 225, 0))
            for arc in self.nodes[n]:
                self.renderArc(surface, camera, cords, arc, (255, 255, 0))

    def renderNode(self, surface, camera, cords, color):
        cords[0] = int(cords[0]) * self.tileWidth + self.tileWidth / 2
        cords[1] = int(cords[1]) * self.tileHeight + self.tileHeight / 2
        pygame.draw.circle(surface, color, camera.apply(cords), 5, 3)

    def renderArc(self, surface, camera, cords, arc, color):
        cordsM = arc.split(',')
        cordsM[0] = int(cordsM[0]) * self.tileWidth + self.tileWidth / 2
        cordsM[1] = int(cordsM[1]) * self.tileHeight + self.tileHeight / 2
        pygame.draw.line(surface, color, camera.apply(cords), camera.apply(cordsM), 2)

    # def renderPath(self, surface, camera, path):
    #     if path is not None:
    #         prevNode = None
    #         for node in path:
    #             cords = node.split(',')
    #             self.renderNode(surface, camera, cords, (255, 0, 0))
    #             if prevNode is not None:
    #                 self.renderArc(surface, camera, cords, prevNode, (255, 0, 0))
    #             prevNode = node

    @staticmethod
    def getGraph(tiledMap: TiledMap, useAllDirections: bool = False):
        graph = {}
        getNeighbors = Graph.getNeighbors8 if useAllDirections else Graph.getNeighbors4
        for row in range(0, tiledMap.rows):
            for col in range(0, tiledMap.cols):
                tile = tiledMap.tileset.getTileInfo(tiledMap.cells[row][col])
                if tile.walkable:
                    graph[str(col) + ',' + str(row)] = getNeighbors(tiledMap, col, row)

        def countNeighbors(key: str):
            return -len(graph[key])

        for nodeKey in graph:
            graph[nodeKey] = sorted(graph[nodeKey], key=countNeighbors)
        return graph

    @staticmethod
    def getNeighbors8(tiledMap: TiledMap, col: int, row: int) -> list:
        nodes = []
        for y in range(row - 1, row + 2):
            if 0 <= y < tiledMap.rows:
                for x in range(col - 1, col + 2):
                    if 0 <= x < tiledMap.cols:
                        if Graph.areContinuous(tiledMap, col, row, x, y):
                            nodes.append(str(x) + ',' + str(y))
        return nodes

    @staticmethod
    def getNeighbors4(tileMap: TiledMap, col: int, row: int) -> list:
        nodes = []
        for cell in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            x = cell[0] + col
            y = cell[1] + row
            if 0 <= y < tileMap.rows and 0 <= x < tileMap.cols:
                if Graph.areContinuous(tileMap, col, row, x, y):
                    nodes.append(str(x) + ',' + str(y))
        return nodes

    @staticmethod
    def areContinuous(tileMap: TiledMap, col: int, row: int, x: int, y: int):
        tile1 = tileMap.tileset.getTileInfo(tileMap.cells[y][x])
        tile2 = tileMap.tileset.getTileInfo(tileMap.cells[y][col])
        tile3 = tileMap.tileset.getTileInfo(tileMap.cells[row][x])
        areContinuous = tile1.walkable and tile2.walkable and tile3.walkable
        return areContinuous

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
        path = self.findShortestPath(start, end)
        path2 = []
        prevNode = None
        node = None
        for nextNode in path:
            if node is not None and not self.areAligned(prevNode, node, nextNode):
                path2.append(node)
            prevNode = node
            node = nextNode
        path2.append(end)
        return path2

    def randomPath(self, start: str = None, end: str = None) -> list:
        nodeStart = choice(list(self.nodes.keys())) if start is None else start
        nodeEnd = choice(list(self.nodes.keys())) if end is None else end
        return self.findShortestPath2(nodeStart, nodeEnd)

    @staticmethod
    def areAligned(nodeA, nodeB, nodeC):
        if nodeA is None:
            return False
        coordsA = nodeA.split(',')
        coordsB = nodeB.split(',')
        coordsC = nodeC.split(',')
        return (
                       coordsA[0] == coordsB[0] == coordsC[0]
               ) or (
                       coordsA[1] == coordsB[1] == coordsC[1]
               )
