import signal
import sys

from constants import anims, fonts, imgs, maps, sounds, tilesets
from game.core import Config, Game, resourceManager, TiledMap
from game.scenes import MainMenu, Playground
from game.ui.gui import gui


# esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    resourceManager.init('assets/', imgs, sounds, fonts, anims, tilesets, maps)
    config = Config('config.json')
    gui.loadSkin(config.skin)
    game = Game(config)
    game.init()
    game.addScene("main", MainMenu(game))
    game.addScene("play", Playground(game))
    game.setScene("main")
    # res.playSong('background1')
    game.run()
    game.quit()


if __name__ == "__main__":
    main()
