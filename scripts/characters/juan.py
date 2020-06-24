from game.core.CharacterWrapper import CharacterWrapper
from game.core.Script import Script
from game.core.Telegram import Telegram


class ScriptCharacter(Script):

    def onInit(self, character: CharacterWrapper):
        character.onInit('Juan')
        character.wander()

    def onUpdate(self, character: CharacterWrapper):
        pass

    def onMessage(self, character: CharacterWrapper, telegram: Telegram):
        pass
