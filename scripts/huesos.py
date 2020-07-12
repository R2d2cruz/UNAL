from game.core.Telegram import Telegram
from game.scripts.CharacterWrapper import CharacterWrapper
from game.scripts.Script import Script


class ScriptCharacter(Script):

    name = 'El malvado Fausto'

    def onInit(self, character: CharacterWrapper):
        character.onInit(self.name)
        character.wander()

    def onUpdate(self, character: CharacterWrapper, neighbors: list):
        # buscar al personaje mas cercano
        if len(neighbors) > 0:
            for neighbor in neighbors:
                if neighbor['type'] == 'character':
                    # si encontro a quien seguir entonces seguirlo
                    character.setSteeringOff()
                    character.goDirectionWithPoint(neighbor['position'])
                    return


    def onMessage(self, character: CharacterWrapper, telegram: Telegram):
        print(self.name, ':', character, telegram.message)

    @staticmethod
    def getAnimName():
        return 'huesos'
