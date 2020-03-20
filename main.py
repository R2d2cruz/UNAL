import pygame
import os
print(os.getcwd())

directory = str(os.getcwd())

pygame.init()


class Game:
    screen = pygame.display.set_mode((1280, 720))
    run = True
    pygame.display.set_icon(pygame.image.load("unallogo.jpg"))
    clock = pygame.time.Clock()

    def __init__(self):
        self.player = Player("Henry")
        self.player.createAnimations()

    def render(self):
        self.player.rezise((self.screen.get_width(), self.screen.get_height()))
        while self.run:
            self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    print(event.key)
                    self.player.update(event.key)
                if event.type == pygame.KEYUP:
                    self.player.wait()
            # RGB - red, green, blue

            self.screen.fill((0, 0, 0))

            self.player.act(self.clock.get_time())
            self.player.draw(self.screen)

            pygame.display.update()


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
    velocityx = 0
    velocityy = 0
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

    def act(self, delta):
        self.x += self.velocityx * delta
        self.y += self.velocityy * delta
        actual = self.animations[self.side]
        actual.update(delta)
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
        self.side -= 4
        self.velocityx = 0
        self.velocityy = 0
        self.animations[self.side].reset()

    def walk(self):
        print("x")
        m = self.switcher.get(self.side)
        self.velocityx = m[0]
        self.velocityy = m[1]

    def createAnimations(self):
        pass


# clase player

class Player(Student):


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
            5: Animation([pygame.transform.scale(pygame.transform.flip(pygame.image.load("sidewalk1.png"), True, False),
                                                 (64, 64)), pygame.transform.scale(pygame.transform.flip(
                pygame.image.load("sidewalk2.png"), True, False), (64, 64))])

        }
        self.actualAnimation = self.animations.get(self.side)
        self.actualFrame = self.actualAnimation.get_frame()
        print("n")

    def rezise(self, screen):  # screen = (width, height)
        self.realX = (screen[0] - self.actualFrame.get_width()) / 2
        self.realY = (screen[1] - self.actualFrame.get_height()) / 2

    def draw(self, screen):
        screen.blit(self.actualFrame, (self.realX, self.realY))


# clase Animation

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


class backGroundMap:
    map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    frames = {}

    #
    # 0 = grass
    # 1 = bricks
    #
    #
    #

    def __init__(self):
        self.frames = {

        }



game = Game()
game.render()
pygame.quit()
