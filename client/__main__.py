import signal
import sys

from client.constants import anims, fonts, imgs, maps, sounds, tilesets
from client.core import Config, Game, resourceManager, TiledMap
from client.scenes import MainMenu, Playground


# esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    resourceManager.init('client/assets/', imgs, sounds, fonts, anims, tilesets, maps)
    game = Game(Config('client/config.json'))
    game.init()
    game.addScene("main", MainMenu(game))
    game.addScene("play", Playground(game, TiledMap('small')))
    game.setScene("main")
    # res.playSong('background1')
    game.run()
    game.quit()


if __name__ == "__main__":
    main()
