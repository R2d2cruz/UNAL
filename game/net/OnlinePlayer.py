from game.core import Character, resourceManager, BaseCamera

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
            (data.get("x"), data.get("y")),
            (0, 24, 34, 32),
            *groups
        )
        self.font = resourceManager.getFont('minecraft', 14)
        self.setName(data.get("n"))
        self.animName = data.get("A")
        if self.animName is not None:
            resourceManager.loadAnimation(self, data.get("A"))
            self.currentClip = onlineTraductor.get(data.get("a"))
        else:
            self.update = self.dummyUpdate
            self.render = self.dummyRender

    def setData(self, data):
        self.setPos(data.get("x"), data.get("y"))
        self.currentClip = onlineTraductor.get(data.get("a"))
        if self.animName is None:
            self.animName = data.get("A")
        if self.animName is not None:
            resourceManager.loadAnimation(self, data.get("A"))
            self.currentClip = onlineTraductor.get(data.get("a"))
            self.update = self.realUpdate
            self.render = self.realRender

    def dummyUpdate(self, deltaTime: float):
        pass

    def realUpdate(self, deltaTime: float):
        super().update(deltaTime)

    def dummyRender(self, surface, camera: BaseCamera):
        pass

    def realRender(self, surface, camera: BaseCamera):
        super().render(surface, camera)
