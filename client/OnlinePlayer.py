from core import Character, Vector2D

onlineTraductor = {
    "stu": "stand_up",
    "std": "stand_down",
    "stl": "stand_left",
    "str": "stand_right",
    "wlu": "up",
    "wld": "down",
    "wll": "left",
    "wlr": "right"
}

class OnlinePlayer(Character):
    def __init__(self, data, *groups):
        super().__init__(
            data.get("n"),
            data.get("A"),
            (data.get("x"), data.get("y")),
            (0, 24, 34, 32),
            *groups
        )
        # self.x = data.get("x")
        # self.y = data.get("y")
        # self.width = 34
        # self.height = 32
        # self.rect.topleft = (self.x, self.y)

    def setPos(self, data):
        self.x = data.get("x")
        self.y = data.get("y")
        self.currentClip = onlineTraductor.get(data.get("a"))
