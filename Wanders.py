from NPC import NPC


class Wander(NPC):

    points = [

    ]

    velocitys = [

    ]

    index = 0

    def update(self):
        if self.rect.toplef == self.points[self.index]:
            self.index += 1
            if self.index == len(self.points):
                self.index = 0
        self.velocity = self.velocitys[self.index]


    def collitions(self, objeto):
        if self.rect.colliderect(objeto):
            self.velocity = [0, 0]
