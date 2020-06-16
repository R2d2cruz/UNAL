from core.Character import Character
from core.Telegram import Telegram
from core.Script import Script


class ScriptCharacter(Script):

    def onInit(self, character: Character, worlRect) -> Character:
        character.setName('Arthur')
        character.setPos(200, 200)
        character.steering.wanderEnabled = True
        print('Cargando Arthur...')

    def onUpdate(self, character: Character):
        pass

    def onMessage(self, character: Character, telegram: Telegram):
        pass

