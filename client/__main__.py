import signal
import sys
# noinspection PyUnresolvedReferences
import core .ResourceManager as res 
# noinspection PyUnresolvedReferences
import core.EntityManager as entManager
# noinspection PyUnresolvedReferences
import core.Hermes as Hermes
# noinspection PyUnresolvedReferences
from core.Game import Game
# noinspection PyUnresolvedReferences
from core.Config import Config
# noinspection PyUnresolvedReferencesx
from Laberinto import Laberinto
# noinspection PyUnresolvedReferences
from scenes.MainMenu import MainMenu
# noinspection PyUnresolvedReferences
from scenes.Playground import Playground
# noinspection PyUnresolvedReferences
from constants import imgs, sounds, fonts, anims, tilesets, maps

# esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    res.init('client/assets/', imgs, sounds, fonts, anims, tilesets, maps)
    entManager.init()
    Hermes.init()
    game = Game(Config('client/config.json'))
    game.init()
    game.addScene("main", MainMenu(game))
    game.addScene("play", Playground(game, Laberinto()))
    game.setScene("main")
    #res.playSong('background1')
    game.run()
    game.quit()

if __name__=="__main__":
    main()