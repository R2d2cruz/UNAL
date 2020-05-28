import signal
import sys
# noinspection PyUnresolvedReferences
import core.ResourceManager as res 
# noinspection PyUnresolvedReferences
from constants import imgs, sounds, fonts, anims, tilesets, maps
# noinspection PyUnresolvedReferences
from core.Game import Game
# noinspection PyUnresolvedReferences
from core.Config import Config
# noinspection PyUnresolvedReferences
from Laberinto import Laberinto
# noinspection PyUnresolvedReferences
from scenes.MainMenu import MainMenu
# noinspection PyUnresolvedReferences
from scenes.Playground import Playground


# esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

res.init('client/assets/', imgs, sounds, fonts, anims, tilesets, maps)
game = Game(Config('client/config.json'))
game.init()
laberinto = Laberinto(game)
game.addScene("main", MainMenu(game))
game.addScene("play", Playground(game, laberinto))
game.setScene("main")
res.playSong('background1')

game.run()
game.quit()
