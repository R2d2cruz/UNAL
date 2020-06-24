from game.core.CharacterWrapper import CharacterWrapper
from game.core.Script import Script
from game.core.Telegram import Telegram


class ScriptCharacter(Script):

    def onInit(self, character: CharacterWrapper):
        character.onInit('Arthur')
        character.wander(0.2)

    def onUpdate(self, character: CharacterWrapper, neighbors: list):
        pass

    def onMessage(self, character: CharacterWrapper, telegram: Telegram):
        pass
