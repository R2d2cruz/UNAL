from game.core.Character import Character
from game.core.Script import Script
from game.core.Telegram import Telegram


class ScriptCharacter(Script):

    def onInit(self, character: Character) -> Character:
        character.setName('Arthur')
        character.setPos(64, 64)
        character.steering.wanderEnabled = True
        character.steering.weightWander = 0.2

    def onUpdate(self, character: Character):
        pass

    def onMessage(self, character: Character, telegram: Telegram):
        pass
