import pygame


class Estudiante:
    name = ""
    attack = 0
    defense = 0
    animations = []
    x = 0
    y = 0
    realX = 320
    realY = 180
    actualFrame = pygame.image()
    side = 0
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
            pygame.K_UP: self.up(),
            pygame.K_DOWN: self.DOWN(),
            pygame.K_RIGHT: self.RIGHT(),
            pygame.K_LEFT: self.LEFT()
        }

    def setAttack(self, attack):
        self.attack = attack

    def getAttack(self):
        return self.attack

    def getName(self):
        return self.name

    def act(self, delta, command):
        self.states(command)
        self.x += self.velocityx
        self.y += self.velocityy

    def draw(self, screen=pygame.display.set_mode((1280, 720))):
        screen.blit(self.actualFrame, (screen.get_window_size()[0] / 2))

    def rezise(self, screen):  # screen = (width, height)
        self.realX = (screen[0] - self.actualFrame.get_width) / 2
        self.realY = (screen[1] - self.actualFrame.get_height) / 2

    def states(self, command):
        self.commands.get(command)

    def up(self):
        self.side = 0
        self.walk()

    def DOWN(self):
        self.side = 1
        self.walk()

    def RIGHT(self):
        self.side = 2
        self.walk()

    def LEFT(self):
        self.side = 3
        self.walk()

    def wait(self):
        self.velocityx = 0
        self.velocityy = 0
        self.actualAnimation = self.animations[self.side]

    def walk(self):
        m = self.switcher.get(self.side)
        self.velocityx = m[0]
        self.velocityy = m[1]

    def createAnimations(self):
        pass
