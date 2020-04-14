import pygame

from NPC import NPC


class Wander(NPC):
    points = [

    ]

    velocities = [

    ]

    index = 1

    def __init__(self, position, points, velocities, reference, *groups):

        super().__init__(position, reference, *groups)
        self.points = points
        self.velocities = velocities
        self.walk = {0: (357, 1, 34, 53), 1: (37, 1, 34, 56), 2: (393, 1, 34, 53), 3: (37, 1, 34, 56)}
        self.backWalk = {0: (285, 1, 34, 54), 1: (1, 1, 34, 56), 2: (321, 1, 34, 54), 3: (1, 1, 34, 56)}
        self.leftWalk = {0: (109, 1, 34, 56), 1: (217, 1, 32, 56), 2: (181, 1, 34, 56), 3: (217, 1, 32, 56)}
        self.rightWalk = {0: (73, 1, 34, 56), 1: (251, 1, 32, 56), 2: (145, 1, 34, 56), 3: (251, 1, 32, 56)}

    def update(self):
        if [self.x, self.y] == self.points[self.index]:
            self.index += 1
            if self.index == len(self.points):
                self.index = 0
        self.velocity = self.velocities[self.index]

    def collitions(self, objeto):
        if self.rect.colliderect(objeto.get_rect()):
            self.velocity = [0, 0]
