import pygame


class Player(pygame.sprite.Sprite):
    KEYDOWN = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right"
    }

    KEYUP = {
        pygame.K_UP: "stand_up",
        pygame.K_DOWN: "stand_down",
        pygame.K_LEFT: "stand_left",
        pygame.K_RIGHT: "stand_right"
    }
    attack = 30
    defense = 20
    HP = 500
    x = 100
    y = 100
    xp = 0
    speed = 3
    velocity = [0, 0]
    isCollide = False
    lastVelocity = [0, 0]
    objectCollition = None

    def __init__(self, position, name="Henry", *groups):
        super().__init__(*groups)
        self.name = name
        self.sheet = pygame.image.load(self.name + ".png")
        self.sheet.set_clip(pygame.Rect(37, 1, 34, 56))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = pygame.Rect(37, 1, 34, 32)  # self.image.get_rect()
        self.rect.topleft = position
        self.frame = 0
        self.front = {0: (37, 1, 34, 56)}
        self.back = {0: (1, 1, 34, 56)}
        self.left = {0: (217, 1, 32, 56)}
        self.right = {0: (251, 1, 32, 56)}
        self.walk = {0: (357, 1, 34, 53), 1: (37, 1, 34, 56), 2: (393, 1, 34, 53), 3: (37, 1, 34, 56)}
        self.backWalk = {0: (285, 1, 34, 54), 1: (1, 1, 34, 56), 2: (321, 1, 34, 54), 3: (1, 1, 34, 56)}
        self.leftWalk = {0: (109, 1, 34, 56), 1: (217, 1, 32, 56), 2: (181, 1, 34, 56), 3: (217, 1, 32, 56)}
        self.rightWalk = {0: (73, 1, 34, 56), 1: (251, 1, 32, 56), 2: (145, 1, 34, 56), 3: (251, 1, 32, 56)}

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(clipped_rect)
        return clipped_rect

    def update(self, direction):
        if direction == "up":
            self.velocity = [0, 4]
            self.clip(self.backWalk)
        if direction == "down":
            self.velocity = [0, -4]
            self.clip(self.walk)
        if direction == "right":
            self.velocity = [-4, 0]
            self.clip(self.rightWalk)
        if direction == "left":
            self.velocity = [4, 0]
            self.clip(self.leftWalk)

        if direction == "stand_up":
            self.clip(self.back)
        if direction == "stand_down":
            self.clip(self.front)
        if direction == "stand_right":
            self.clip(self.right)
        if direction == "stand_left":
            self.clip(self.left)

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.update(self.KEYDOWN.get(event.key))

        if event.type == pygame.KEYUP:
            self.velocity = [0, 0]
            self.update((self.KEYUP.get(event.key)))

    def act(self):
        if self.lastVelocity != self.velocity:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        # return self.velocity == [0, 0]

    def blit(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 0, 0), self.get_rect())

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_velocity(self):
        return self.velocity

    def collitions(self, object):
        if self.get_rect().colliderect(object.get_rect()) == 1:
            if not self.isCollide:
                self.velocity = [0, 0]
                self.isCollide = True
                self.objectCollition = object

            else:
                if object == self.objectCollition:
                    if (object.get_rect().x - self.get_rect().x) < object.get_rect().width:
                        vel = [0, -4 if object.get_rect().y > self.get_rect().y else 4]
                    else:
                        vel = [-4 if object.get_rect().y > self.get_rect().y else 4, 0]

                    if self.velocity == vel:
                        self.velocity = [0, 0]
                    elif self.get_rect().colliderect(object.get_rect()):
                        self.isCollide = False

        #print(self.isCollide)

    def overlap(self, x1, d1, x2, d2):
        return x1 + d1 > x2 if x1 < x2 else x2 + d2 > x1

    def get_rect(self):
        return pygame.Rect((self.rect.x, self.rect.y + 32, 34, 32))

    def prox_rect(self):
        x = self.rect.x + self.velocity[0]
        print(x)
        y = self.rect.y + self.velocity[1]
        return pygame.Rect((x, y, 34, 32))
