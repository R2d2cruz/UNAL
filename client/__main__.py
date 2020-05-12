import pygame
import os
import signal
import sys

from core.Game import Game
from Config import Config

## esta funcion sirve para que el juego se cierre cuando el usuario presiona Ctr + C en la consola
def signal_handler(sig, frame):
    print("\n\nCada vez que presionas Ctrl + C para cerrar este juego el sistema mata un gatito🐱! 😭😭😭")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

game = Game(Config())
game.run()
pygame.quit()

