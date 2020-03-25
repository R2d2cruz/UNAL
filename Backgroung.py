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

    def handleEvents(self, event):
        self.player.handle_event(event)

    def update(self):
        self.player.collitions([self.characters, self.objects])
        for i in self.characters:
            i.act()
        if not self.player.act():
            self.changeCoor(self.player.get_x(), self.player.get_y())

    def blit(self, screen):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                screen.blit(self.frames.get(self.map[i][j]), (self.x + (self.rect * j), self.y + (self.rect * i)))
        self.player.blit(screen)
        for k in self.characters:
            k.blit()
        for k in self.objects:
            k.blit()
