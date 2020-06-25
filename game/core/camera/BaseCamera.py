class BaseCamera:
    def __init__(self):
        pass

    def follow(self, target):
        pass

    def apply(self, pos):
        return pos

    def unapply(self, pos):
        return pos

    def update(self, deltaTime: float):
        pass

    def render(self, surface):
        pass
