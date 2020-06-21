from .core import Character

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
        self.currentClip = onlineTraductor.get(data.get("a"))

    def setData(self, data):
        self.setPos(data.get("x"), data.get("y"))
        self.currentClip = onlineTraductor.get(data.get("a"))
