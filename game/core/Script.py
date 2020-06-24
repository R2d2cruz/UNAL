from .Character import Character


class Script:
    def __init__(self):
        self.name = None

    def onInit(self, character: Character):
        pass

    def onUpdate(self, neighbors: list):
        pass
