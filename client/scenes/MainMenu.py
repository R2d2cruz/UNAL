import pygame
import core.ResourceManager as res

from core.Scene import Scene
from core.Game import Game
from core.ui.InputBox import InputBox
from core.ui.Button import Button
from core.ui.Label import Label
from core.AnimatedEntity import AnimatedEntity

class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.font = res.getFont('minecraft', 36)

        rect = pygame.Rect(0, 0, 450, 80)

        rect.center = (game.config.windowWidth / 4, game.config.windowHeight / 3)
        self.buttonPlay = Button(rect.x, rect.y, rect.w, rect.h, self.font, 'Quiero jugar!')
        self.buttonPlay.onClick = self.onGoPlay

        rect.center = (game.config.windowWidth / 4, game.config.windowHeight * 2 / 3)
        self.buttonQuit = Button(rect.x, rect.y, rect.w, rect.h, self.font, 'Tengo miedo!, me salgo')
        self.buttonQuit.onClick = self.onGoQuit

        rect.center = (game.config.windowWidth * 3 / 4, - 55 + game.config.windowHeight * 2 / 3)
        self.label1 = Label(rect.x, rect.y, rect.w, rect.h, self.font, 'Nombre del heroe:', (0, 128, 255))
        
        rect.center = (game.config.windowWidth * 3 / 4, game.config.windowHeight * 2 / 3)
        self.inputBox1 = InputBox(rect.x, rect.y, rect.w, rect.h, self.font)

        self.anim = AnimatedEntity()
        self.anim.x, self.anim.y= (game.config.windowWidth * 3 / 4, game.config.windowHeight / 3)
        self.anim.loadAnimation(res.getRandomCharAnimFile())
        self.anim.currentClip = 'down'

        self.done = False
        self.controls = [
            self.buttonPlay,
            self.buttonQuit,
            self.label1,
            self.inputBox1,
            self.anim
        ]

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: preguntarle al usuario si esta seguro de salir
                self.game.quit()
                return
        for box in self.controls:
            box.handleEvent(event)

    def handleMessage(self, message):
        pass

    def update(self):
        for box in self.controls:
            box.update()

    def render(self, screen):
        screen.fill((30, 30, 30))
        for control in self.controls:
            control.render(screen)
        # TODO: si el cliente está conectado mostrar a que servidor esta conectado, sino entonces indicar que no esta conectado

    def onEnterScene(self):
        if (self.game.player is not None) and (self.game.player.name is None):
            print('loading')
            self.game.loadSettings()
        print('setting the name', self.game.player.name)
        self.inputBox1.text = self.game.player.name

    def onGoPlay(self, sender):
        # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
        self.game.player.set_name(self.inputBox1.text)
        self.game.saveSettings()
        if not self.game.client.connected:
            if not self.game.client.connect(self.game.player.name):
                # TODO: en vez de finaizar aqui simplemente se muestra un mensaje en pantalla indicandole al usuario que no se pudo conectar
                # TODO: un boton en la pantalla permite salir, esta linea va allá
                pass
        if self.game.client.connected:
            self.game.setScene("play")

    def onEnterName(self, sender):
        pass

    def onGoQuit(self, sender):
        self.game.quit()