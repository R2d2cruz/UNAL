from game.core import Character


class Player(Character):

    def __init__(self, name, animationName, position, collisionRect):
        super().__init__(name, animationName, position, collisionRect)
        self.health = 20
        self.xp = 0
