import json

import pygame

from ..core import AnimatedEntity, Game, NullCamera, Scene, resourceManager
from ..ui import Button, InputBox, Label, GridContainer, Container, BoxContainer


class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.camera = NullCamera()
        self.font = resourceManager.getFont('minecraft', 36)
        self.index = 0
        self.ui = self.createUI()
        self.done = False

    def createUI(self):
        grid1 = GridContainer(0, 0, self.game.surface.get_width() / 2, self.game.surface.get_height())
        grid1.setGrid(3, 1)

        buttonPlay = Button(0, 0, 450, 70, self.font, 'Quiero jugar!')
        buttonPlay.onClick = self.onGoPlay
        grid1.addControl(buttonPlay, (0, 0))

        buttonEdit = Button(0, 0, 450, 70, self.font, 'Editar mapa')
        buttonEdit.onClick = self.onEdit
        grid1.addControl(buttonEdit, (1, 0))

        buttonQuit = Button(0, 0, 450, 70, self.font, 'Tengo miedo!, me salgo')
        buttonQuit.onClick = self.onGoQuit
        grid1.addControl(buttonQuit, (2, 0))

        box1 = BoxContainer(BoxContainer.VERTICAL, 1 + self.game.surface.get_width() / 2, 0,
                            self.game.surface.get_width() / 2, self.game.surface.get_height())

        musicButton = Button(0, 0, 256, 64, self.font, 'Music: ON')
        musicButton.onClick = self.onMusicButton
        box1.addControl(musicButton)

        soundButton = Button(0, 0, 256, 64, self.font, 'Sounds: ON')
        soundButton.onClick = self.onSoundButton
        box1.addControl(soundButton)

        label1 = Label(0, 0, 450, 70, self.font, 'Nombre del heroe:', (255, 255, 255))
        box1.addControl(label1)

        inputBox1 = InputBox(0, 0, 450, 70, self.font)
        inputBox1.name = 'playerName'
        inputBox1.onChange = self.onChangeName
        box1.addControl(inputBox1)

        grid2 = GridContainer(0, 0, 450, 70)
        grid2.setGrid(1, 3)

        leftListButton = Button(0, 0, 64, 64, self.font, '<')
        leftListButton.onClick = self.goToLeftList
        grid2.addControl(leftListButton, (0, 0))

        anim = AnimatedEntity()
        anim.name = 'selectAnim'
        anim.currentClip = 'down'
        self.changeAnim(anim)
        grid2.addControl(anim, (0, 1))

        rightListButton = Button(0, 0, 64, 64, self.font, '>')
        rightListButton.onClick = self.goToRightList
        grid2.addControl(rightListButton, (0, 2))
        box1.addControl(grid2)

        ui = Container(0, 0, self.game.surface.get_width(), self.game.surface.get_height())
        ui.addControl(grid1)
        ui.addControl(box1)
        # ui.addControl(grid3)
        return ui

    def onKeyUp(self, event):
        if event.key == pygame.K_ESCAPE:
            # TODO: preguntarle al usuario si esta seguro de salir
            self.game.quit()

    def handleMessage(self, message):
        pass

    def render(self, surface: pygame.Surface):
        surface.fill((30, 30, 30))
        self.ui.render(surface, self.camera)
        # TODO: si el cliente está conectado mostrar a que servidor esta conectado, sino entonces indicar que no esta
        #  conectado

    def onEnterScene(self, data: dict = None):
        self.loadSettings()

    def onEdit(self, sender):
        resourceManager.playSound('title')
        self.game.setScene('edit', dict(
            # game=self.game,
            mapName=self.game.config.map
        ))

    def onGoPlay(self, sender):
        control = self.ui.getControlByName('playerName')
        if not self.game.client.connected:
            if not self.game.client.connect(control.text):
                # TODO: en vez de finaizar aqui simplemente se muestra un mensaje en pantalla indicandole al usuario
                #  que no se pudo conectar un boton en la pantalla permite salir, esta linea va allá
                resourceManager.playSound('error')
                pass
        if self.game.client.connected:
            # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
            animName = resourceManager.getAnimName(self.index)
            self.saveSettings()
            resourceManager.playSound('title')
            self.game.setScene('play', dict(
                playerName=control.text,
                game=self.game,
                animName=animName,
                mapName=self.game.config.map
            ))

    def onGoQuit(self, sender):
        resourceManager.playSound('select')
        # demorar aqui un poco, tal vez mostrar una animacion o algo mientras sale
        pygame.time.delay(100)
        self.game.quit()

    def goToLeftList(self, sender):
        resourceManager.playSound('select')
        self.index -= 1
        if self.index < 0:
            self.index = resourceManager.getAnimCount() - 1
        self.changeAnim()

    def goToRightList(self, sender):
        resourceManager.playSound('select')
        self.index += 1
        if self.index > (resourceManager.getAnimCount() - 1):
            self.index = 0
        self.changeAnim()

    @staticmethod
    def onChangeName(sender):
        resourceManager.playSound('hit-key')

    @staticmethod
    def onMusicButton(sender: Button):
        enable = "ON" if resourceManager.flipEnableMusic() else "OFF"
        resourceManager.playSound('select')
        sender.text = "Music: " + enable

    @staticmethod
    def onSoundButton(sender: Button):
        enable = "ON" if resourceManager.flipEnableSound() else "OFF"
        resourceManager.playSound('select')
        sender.text = "Sounds: " + enable

    def changeAnim(self, entity: AnimatedEntity = None):
        if entity is None:
            entity = self.ui.getControlByName('selectAnim')
        if entity is not None:
            entity.loadAnimation(resourceManager.getAnimFile(resourceManager.getAnimName(self.index)))
            entity.currentClip = 'down'

    def loadSettings(self):
        with open('saves/player.save', 'r') as infile:
            data = json.load(infile)
            playerName = data.get('name')
            if playerName is None:
                playerName = resourceManager.getRandomCharAnimName()
            control = self.ui.getControlByName('playerName')
            control.text = playerName

    def saveSettings(self):
        control = self.ui.getControlByName('playerName')
        with open('saves/player.save', 'w') as outfile:
            json.dump(dict(name=control.text), outfile)
