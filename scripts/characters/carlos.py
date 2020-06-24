from game.core.Script import Script
from game.core.Telegram import Telegram
from game.core.characterWrapper import wrapper


class ScriptCharacter(Script):

    def onInit(self, character: wrapper):
        character.onInit('Carlos')
        character.wander()

    def onUpdate(self, character: wrapper):
        pass

    def onMessage(self, character: wrapper, telegram: Telegram):
        pass
