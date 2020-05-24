import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.target = None

    def follow(self, target):
        self.target = target

    def apply(self, rect):
      if type(rect) == pygame.Rect:
        return rect.move(self.camera.topleft)
      elif type(rect) == tuple:
        return (rect[0] + self.camera.x, rect[1] + self.camera.y)

    def update(self):
        if self.target is not None:
            x = -self.target.x - int(self.target.width / 2)
            y = -self.target.y - int(self.target.height / 2)
            # # limit scrolling to map size
            #x = min(0, x)  # left
            #y = min(0, y)  # top
            #x = max(-(self.width - self.dest.width), x)  # right
            #y = max(-(self.height - self.dest.height), y)  # bottom
            self.camera.x = x + int(self.width / 2)
            self.camera.y = y + int(self.height / 2)
