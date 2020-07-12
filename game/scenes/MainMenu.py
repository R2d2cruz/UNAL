import json

import pygame

from ..core import AnimatedEntity, Game, NullCamera, Scene, resourceManager
from ..net.Client import Client
from ..ui import Button, InputBox, Label, GridContainer, Container, BoxContainer, AnimatedBox
from ..ui.ScrollBar import ScrollBar


class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.camera = NullCamera()
        self.font = resourceManager.getFont('MinecraftRegular', 36)
        self.index = 0
        self.anim = None
        self.ui = self.createUI()
        self.done = False
        self.client = Client(game.config)

    def createUI(self):
        grid1 = GridContainer(0, 0, self.game.windowWidth / 2, self.game.windowHeight)
        grid1.setGrid(3, 1)

        buttonPlay = Button(0, 0, 450, 70, self.font, 'Quiero jugar!')
        buttonPlay.onClick = self.onGoPlay
        grid1.addControl(buttonPlay, (0, 0))

        buttonQuit = Button(0, 0, 450, 70, self.font, 'Tengo miedo!, me salgo')
        buttonQuit.onClick = self.onClickQuit
        grid1.addControl(buttonQuit, (2, 0))

        box1 = BoxContainer(BoxContainer.VERTICAL, 1 + self.game.windowWidth / 2, 0,
                            self.game.windowWidth / 2, self.game.windowHeight)

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

        animation = AnimatedBox(0, 0, 100, 100)
        self.anim = AnimatedEntity()
        self.anim.currentClip = 'down'
        resourceManager.loadAnimation(self.anim, resourceManager.getAnimName(self.index))
        animation.animation = self.anim
        animation.name = 'selectAnim'
        box1.addControl(animation)

        scroll1 = ScrollBar(0, 0, 200, 32, self.font)
        scroll1.minValue = 1
        scroll1.maxValue = resourceManager.getAnimCount()
        scroll1.step = 1
        scroll1.onChange = self.onChangeAnim
        box1.addControl(scroll1)

        ui = Container(0, 0, self.game.windowWidth, self.game.windowHeight)
        ui.addControl(grid1)
        ui.addControl(box1)

        # ui.addControl(grid3)
        return ui

    def onKeyUp(self, event):
        if event.key == pygame.K_ESCAPE:
            # TODO: preguntarle al usuario si esta seguro de salir
            self.game.quit()

    def update(self, deltaTime: float):
        if self.anim:
            self.anim.update(deltaTime)

    def render(self, surface: pygame.Surface):
        surface.fill((30, 30, 30))
        self.ui.render(surface, self.camera)
        # TODO: si el cliente está conectado mostrar a que servidor esta conectado, sino entonces indicar que no esta
        #  conectado

    def onEnterScene(self, data: dict = None):
        self.loadSettings()

    def onEdit(self, event, sender):
        resourceManager.playSound('title')
        self.game.setScene('edit', dict(
            # game=self.game,
            mapName=self.game.config.map
        ))

    def onGoPlay(self, event, sender):
        control = self.ui.getControlByName('playerName')
        if not self.client.connected:
            if not self.client.connect(control.text):
                # TODO: en vez de finaizar aqui simplemente se muestra un mensaje en pantalla indicandole al usuario
                #  que no se pudo conectar un boton en la pantalla permite salir, esta linea va allá
                resourceManager.playSound('error')
                pass
        if self.client.connected:
            # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
            animName = resourceManager.getAnimName(self.index)
            self.saveSettings()
            resourceManager.playSound('title')
            self.game.setScene('play', dict(
                playerName=control.text,
                game=self.game,
                animName=animName,
                mapName=self.game.config.map,
                client=self.client
            ))

    def onClickQuit(self, event, sender):
        resourceManager.playSound('select')
        # demorar aqui un poco, tal vez mostrar una animacion o algo mientras sale
        pygame.time.delay(100)
        self.game.quit()

    def onChangeAnim(self, sender):
        self.index = sender.value - 1
        control = self.ui.getControlByName('selectAnim')
        if control is not None:
            resourceManager.loadAnimation(control.animation, resourceManager.getAnimName(self.index))
            control.animation.currentClip = 'down'
            control.refresh()

    @staticmethod
    def onChangeName(sender):
        resourceManager.playSound('hit-key')

    @staticmethod
    def onMusicButton(event, sender: Button):
        enable = "ON" if resourceManager.flipEnableMusic() else "OFF"
        resourceManager.playSound('select')
        sender.text = "Music: " + enable

    @staticmethod
    def onSoundButton(event, sender: Button):
        enable = "ON" if resourceManager.flipEnableSound() else "OFF"
        resourceManager.playSound('select')
        sender.text = "Sounds: " + enable

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
