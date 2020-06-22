from client.core.Character import Character
from client.core.Script import Script
from client.core.Telegram import Telegram


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
