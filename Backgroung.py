import pygame


class Background:
    map = [

    ]
    frames = {

    }

    jumpPoints = [

    ]

    objects = [

    ]

    characters = [

    ]

    player = None
    x = 0
    y = 0
    rect = 32

    def changeCoor(self, x, y):
        self.x = x
        self.y = y
        for i in self.characters:
            i.change_reference_point([self.x, self.y])
        for i in self.objects:
            i.change_reference_point([self.x, self.y])

    def handleEvents(self, event):
        self.player.handle_event(event)

    def update(self):
        self.collitions()
        for i in self.characters:
            i.update()
            i.act()
        for i in self.objects:
            self.player.collitions(i)
        if not self.player.act():
            self.changeCoor(self.player.get_x(), self.player.get_y())

    def blit(self, screen):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                screen.blit(self.frames.get(self.map[i][j]), (self.x + (self.rect * j), self.y + (self.rect * i)))
        for k in self.characters:
            k.blit(screen)
        for k in self.objects:
            k.blit(screen)
        self.player.blit(screen)

    def collitions(self):
        for i in range(len(self.characters)):
            self.player.collitions(self.characters[i])
            self.characters[i].collitions(self.player)
