from core.Character import Character
from core.Telegram import Telegram
from core.Script import Script


class ScriptCharacter(Script):

    def onInit(self, character: Character) -> Character:
        character.setName('Arthur')
        character.setPos(64, 64)
        character.steering.wanderEnabled = True

    def onUpdate(self, character: Character):
        pass

    def onMessage(self, character: Character, telegram: Telegram):
        pass

