import pygame
from core.Scene import Scene
from core.Game import Game
from core.InputBox import InputBox

class MainMenu(Scene):
    def __init__(self, game: Game):
        #self.clock = pg.time.Clock()
        font = game.res.getFont('minecraft', 32)
        self.inputBox1 = InputBox(100, 100, 140, 32, font)
        self.inputBox1.onEnter = self.onEnterName
        self.inputBoxes = [self.inputBox1]
        self.done = False
        self.game = game

    def handleEvent(self, event):
        for box in self.inputBoxes:
            box.handle_event(event)

    def update(self):
        for box in self.inputBoxes:
            box.update()
    
    def render(self, screen):
        screen.fill((30, 30, 30))
        for box in self.inputBoxes:
            box.draw(screen)

    def onEnterName(self, sender):
        self.game.player.set_name(sender.text)
        self.game.connectClient()
        self.game.setScene("play")
