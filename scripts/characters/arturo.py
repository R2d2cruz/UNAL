from core.Character import Character
from core.Telegram import Telegram
from core.Script import Script


class Arturo(Script):

    def onInit(self, character: Character, worlRect) -> Character:
        character.setName('Arthur')
        character.setPos(200, 200)
        character.steering.wanderEnabled = True
        print('Cargando Arthur...')

    def onUdpdate(self, character: Character):
        print('onUpdate', character.name)

    def onMessage(self, character: Character, telegram: Telegram):
        pass

