import signal
import sys

from constants import imgs
from game.core import Config, Game, resourceManager
from game.scenes import Editor
from game.ui.gui import gui


# esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    resourceManager.init('assets/', imgs)
    config = Config('config.json')
    gui.loadSkin(config.skin)
    game = Game(config)
    game.init()
    game.addScene("edit", Editor(game))
    game.setScene("edit", dict(mapName=config.map))
    game.run()
    game.quit()


if __name__ == "__main__":
    main()
