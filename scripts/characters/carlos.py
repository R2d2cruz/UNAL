from game.core.Character import Character
from game.core.Script import Script
from game.core.Telegram import Telegram


class ScriptCharacter(Script):

    def onInit(self, character: Character):
        character.setName('Carlos')
        character.setPos(128, 128)
        character.steering.wanderEnabled = True
        character.steering.weightWander = 0.5

    def onUpdate(self, character: Character):
        pass

    def onMessage(self, character: Character, telegram: Telegram):
        pass
