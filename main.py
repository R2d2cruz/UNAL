import pygame
import os
from Player import Player
from UniversityMap import UniversityMap

print(os.getcwd())
directory = str(os.getcwd())
pygame.init()


class Game:
    screen = pygame.display.set_mode((1280, 720))
    run = True
    pygame.display.set_icon(pygame.image.load("unallogo.jpg"))
    clock = pygame.time.Clock()

    def __init__(self):
        #self.player = Player((640, 360))
        self.map = UniversityMap()

    def render(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.map.handleEvents(event)
            self.map.update()
            #self.player.handle_event(event)
            #if not self.player.act():
                #self.map.changeCoor(self.player.get_x(), self.player.get_y())
            self.screen.fill((0, 0, 0))
            #blits
            self.map.blit(self.screen)
            #self.player.blit(self.screen)
            pygame.display.update()
            self.clock.tick(30)

# clase estudiantes


class Student:
    name = ""
    attack = 0
    defense = 0
    animations = []
    x = 0
    y = 0
    actualFrame = None
    side = 1
    velocityX = 0
    velocityY = 0
    actualAnimation = None

    # 0 = front
    # 1 = back
    # 2 = right
    # 3 = left

    switcher = {
        0: (0, -5),
        1: (0, 5),
        2: (5, 0),
        3: (-5, 0)
    }

    commands = {
    }

    def __init__(self, name):
        self.name = name
        self.commands = {
            pygame.K_UP: self.up,
            pygame.K_DOWN: self.DOWN,
            pygame.K_RIGHT: self.RIGHT,
            pygame.K_LEFT: self.LEFT
        }

    def setAttack(self, attack):
        self.attack = attack

    def getAttack(self):
        return self.attack

    def getName(self):
        return self.name

    def act(self):
        self.x += self.velocityX
        self.y += self.velocityY
        actual = self.animations[self.side]
        self.actualFrame = actual.get_frame()

    def draw(self, screen):
        screen.blit(self.actualFrame, (self.x, self.y))

    def update(self, key):
        print("in update")
        self.commands.get(key, lambda: None)()

    def up(self):
        self.side = 0
        self.walk()

    def DOWN(self):
        print("down")
        self.side = 1
        self.walk()

    def RIGHT(self):
        self.side = 2
        self.walk()

    def LEFT(self):
        self.side = 3
        self.walk()

    def wait(self):
        self.velocityX = 0
        self.velocityY = 0
        self.animations[self.side].reset()

    def walk(self):
        print("x")
        m = self.switcher.get(self.side)
        self.velocityX = m[0]
        self.velocityY = m[1]

    def createAnimations(self):
        pass


# clase player

class player(Student):

    realX = 320
    realY = 180

    def createAnimations(self):
        self.animations = {
            1: Animation([pygame.transform.scale(pygame.image.load("frent.png"), (64, 64))]),
            0: Animation([pygame.transform.scale(pygame.image.load("back.png"), (64, 64))]),
            2: Animation([pygame.transform.scale(pygame.image.load("side.png"), (64, 64))]),
            3: Animation(
                [pygame.transform.scale(pygame.transform.flip(pygame.image.load("side.png"), True, False), (64, 64))]),
            4: Animation([pygame.transform.scale(pygame.image.load("sidewalk1.png"), (64, 64)), pygame.transform.scale(
                pygame.image.load("sidewalk2.png"), (64, 64))]),
            5: Animation([pygame.transform.scale(
                   pygame.transform.flip(
                       pygame.image.load("sidewalk1.png"), True, False
                   ), (64, 64)
                 ), pygame.transform.scale(
                    pygame.transform.flip(pygame.image.load("sidewalk2.png"), True, False), (64, 64)
                )
            ])

        }
        self.actualAnimation = self.animations.get(self.side)
        self.actualFrame = self.actualAnimation.get_frame()
        print("n")

    def resize(self, screen):  # screen = (width, height)
        self.realX = (screen[0] - self.actualFrame.get_width()) / 2
        self.realY = (screen[1] - self.actualFrame.get_height()) / 2

    def draw(self, screen):
        screen.blit(self.actualFrame, (self.realX, self.realY))


# class Animation

class Animation:
    frames = []
    lapse = 0
    N = 0
    loop = False
    time = 0

    def __init__(self, frames, loop=False, lapse=1):
        self.frames = frames
        self.lapse = lapse
        self.N = len(frames)
        self.loop = loop

    def update(self, delta):
        self.time += delta

    def reset(self):
        self.time = 0

    def get_frame(self):
        n = int(self.time / self.lapse)
        if n > self.N:
            if self.loop:
                n = n % self.N
            else:
                n = self.N
            return self.frames[n - 1]
        else:
            return self.frames[n]





game = Game()
game.render()
pygame.quit()
