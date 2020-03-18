import pygame

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
        while self.run:
            self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                self.player.act(self.clock.get_time())
                if event.type == pygame.KEYDOWN:
                    self.player.commands.get(event.key)
                if event.type == pygame.KEYUP:
                    self.player.wait()
            # RGB - red, green, blue

            self.player.draw(self.screen)
            self.screen.fill((0, 0, 0))
            pygame.display.update()


# clase estudiantes


class Estudiante:
    name = ""
    attack = 0
    defense = 0
    animations = []
    x = 0
    y = 0
    realX = 320
    realY = 180
    actualFrame = None
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

    def act(self, delta):
        self.x += self.velocityx
        self.y += self.velocityy
        actual = self.animations[self.side]
        actual.update(delta)
        self.actualFrame = actual.get_frame()

    def draw(self, screen=pygame.display.set_mode((1280, 720))):
        screen.blit(self.actualFrame, (50, 50))

    def rezise(self, screen):  # screen = (width, height)
        self.realX = (screen[0] - self.actualFrame.get_width) / 2
        self.realY = (screen[1] - self.actualFrame.get_height) / 2


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
        self.animations[self.side].reset()

    def walk(self):
        m = self.switcher.get(self.side)
        self.velocityx = m[0]
        self.velocityy = m[1]
        

    def createAnimations(self):
        pass


# clase player

class Player(Estudiante):

    def createAnimations(self):
        self.animations = {
            0: Animation([pygame.image.load("frent.png")]),
            1: Animation([pygame.image.load("back.png")]),
            2: Animation({pygame.image.load("side.png")}),
            3: Animation({pygame.transform.flip(pygame.image.load("side.png"), True, False)}),
            4: Animation({pygame.image.load("sidewalk1.png"), pygame.image.load("sidewalk2.png")}),
            5: Animation({pygame.transform.flip(pygame.image.load("sidewalk1.png"), True, False), pygame.transform.flip(pygame.image.load("sidewalk2.png"), True, False)})

        }
        self.actualAnimation = self.animations.get(self.side)
        self.actualFrame = self.actualAnimation.get_frame()
        print("n")


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


game = Game()
game.render()
pygame.quit()
