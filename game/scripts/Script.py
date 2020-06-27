from game.core import Telegram
from .CharacterWrapper import CharacterWrapper


class Script:
    def __init__(self):
        self.name = None

    def onInit(self, character: CharacterWrapper):
        pass

    def onUpdate(self, character: CharacterWrapper, neighbors: list):
        pass

    def onMessage(self, character: CharacterWrapper, telegram: Telegram):
        pass
