from game.core.Telegram import Telegram
from game.scripts.CharacterWrapper import CharacterWrapper
from game.scripts.Script import Script


class ScriptCharacter(Script):

    name = 'Carlos'

    def onInit(self, character: CharacterWrapper):
        character.onInit(self.name)
        character.wander()

    def onUpdate(self, character: CharacterWrapper, neighbors: list):
        pass

    def onMessage(self, character: CharacterWrapper, telegram: Telegram):
        pass

    @staticmethod
    def getAnimName():
        return 'charly'
