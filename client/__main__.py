import pygame
import os
import signal
import sys

import os

if os.name != "nt":
    # noinspection PyUnresolvedReferences
    from constants import imgs, sounds, fonts, anims, tilesets, maps
    # noinspection PyUnresolvedReferences
    from core.Game import Game
    # noinspection PyUnresolvedReferences
    from core.Config import Config
    from core.ResourceHandler import ResourceHandler
    from Laberinto import Laberinto
    from scenes.MainMenu import MainMenu
    from scenes.Playground import Playground
else:
    from client.constants import imgs, sounds, fonts, anims, tilesets,maps
    from client.core.Game import Game
    from client.core.Config import Config
    from client.core.ResourceHandler import ResourceHandler
    from client.Laberinto import Laberinto
    from client.scenes.MainMenu import MainMenu
    from client.scenes.Playground import Playground


# esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if os.name != 'nt':
    resPath = 'client/assets/'
else:
    resPath = '../client/assets/'

res = ResourceHandler(resPath, imgs, sounds, fonts, anims, tilesets, maps)

game = Game(res, Config('client/config.json'))
game.init()
game.addScene("main", MainMenu(game))

laberinto = Laberinto(game)
game.addScene("play", Playground(laberinto))
game.setScene("main")
game.setPlayer(laberinto.player)
game.run()
pygame.quit()

