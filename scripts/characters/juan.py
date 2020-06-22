from client.core.Character import Character
from client.core.Script import Script
from client.core.Telegram import Telegram


class ScriptCharacter(Script):

    def onInit(self, character: Character):
        character.setName('Juan')
        character.setPos(192, 192)
        character.steering.wanderEnabled = True

    def onUpdate(self, character: Character):
        pass

    def onMessage(self, character: Character, telegram: Telegram):
        pass
