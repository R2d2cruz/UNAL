import json

# movements:
# std = stand down
# stu = stand up
# str = stand right
# stl = stand left
# wld = walk down
# wlu = walk up
# wll = walk left
# wlr = walk right


class Player:

    prevx = 0
    prevy = 0
    prevMovement = "std"
    x = 0
    y = 0
    movement = "std"

    def __init__(self, name):
        self.name = name

    def update(self, information):
        message = json.loads(information)
        self.x = message.get("x")
        self.y = message.get("y")
        self.movement = message.get("a")

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "a": self.movement,
            "n": self.name
        }
