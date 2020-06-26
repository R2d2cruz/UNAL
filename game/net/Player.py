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
    def __init__(self, name: str, anim: str):
        self.prevMovement = "std"
        self.x = 0
        self.y = 0
        self.movement = "std"
        self.id = id
        self.name = name
        self.animName = anim

    def update(self, data):
        self.x = data.get("x")
        self.y = data.get("y")
        self.movement = data.get("a")
        self.animName = data.get("A")

    def toDict(self):
        return dict(
            id=self.id,
            x=self.x,
            y=self.y,
            a=self.movement,
            n=self.name,
            A=self.animName
        )
