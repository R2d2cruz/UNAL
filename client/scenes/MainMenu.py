import pygame
from core.Scene import Scene
from core.Game import Game
from core.ui.InputBox import InputBox
from core.ui.Button import Button
from core.ui.Label import Label


class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.font = game.res.getFont('minecraft', 36)
        self.label1 = Label(160, 90, 500, 46, self.font, 'Nombre del heroe:', (0, 128, 255))
        self.inputBox1 = InputBox(160, 140, 500, 46, self.font)
        self.button1 = Button(670, 140, 140, 48, self.font, 'Entrar')
        self.button1.onClick = self.onEnterName
        self.done = False
        self.controls = [
            self.label1,
            self.inputBox1,
            self.button1
        ]

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: preguntarle al usuario si esta seguro de salir
                self.game.quit()
                return
        for box in self.controls:
            box.handleEvents(event)

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

    def onEnterName(self, sender):
        # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
        self.game.player.set_name(self.inputBox1.text)
        if not self.game.client.connected:
            if not self.game.client.connect(self.game.player.name):
                # TODO: en vez de finaizar aqui simplemente se muestra un mensaje en pantalla indicandole al usuario que no se pudo conectar
                # TODO: un boton en la pantalla permite salir, esta linea va allá
                pass
        if self.game.client.connected:
            self.game.setScene("play")