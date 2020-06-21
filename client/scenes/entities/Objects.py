from core import Entity, resourceManager


class Rock(Entity):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = resourceManager.loadImage("ts1", (64, 32, 32, 32))


class Tree(Entity):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = resourceManager.loadImage("ts1", (0, 0, 32, 64))
