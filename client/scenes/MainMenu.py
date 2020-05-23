import pygame
from core.Scene import Scene
from core.Game import Game
from core.InputBox import InputBox


class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.font = game.res.getFont('minecraft', 48)
        self.label = self.font.render('Nombre del heroe:', True, (0, 128, 255))
        self.inputBox1 = InputBox(160, 140, 500, 48, self.font)
        self.inputBox1.onEnter = self.onEnterName
        self.inputBoxes = [self.inputBox1]
        self.done = False

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: preguntarle al usuario si esta seguro de salir
                self.game.quit()
                return
        for box in self.inputBoxes:
            box.handleEvents(event)

    def update(self):
        for box in self.inputBoxes:
            box.update()

    def render(self, screen):
        screen.fill((30, 30, 30))
        screen.blit(self.label, (160, 80))
        for box in self.inputBoxes:
            box.render(screen)
        # TODO: si el cliente está conectado mostrar a que servidor esta conectado, sino entonces indicar que no esta conectado

    def onEnter(self):
        pass

    def onEnterName(self, sender):
        # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
        self.game.player.set_name(sender.text)
        if not self.game.client.connected:
            if not self.game.client.connect(self.game.player.name):
                # TODO: en vez de finaizar aqui simplemente se muestra un mensaje en pantalla indicandole al usuario que no se pudo conectar
                self.game.quit() # TODO: un boton en la pantalla permite salir, esta linea va allá
        if self.game.client.connected:
            self.game.setScene("play")