import pygame

from ..core import AnimatedEntity, Game, NullCamera, Scene, resourceManager
from ..ui import Button, InputBox, Label, GridContainer, Container, BoxContainer


class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.camera = NullCamera()
        self.font = resourceManager.getFont('minecraft', 36)
        self.index = 0
        rect = pygame.Rect(0, 0, 450, 80)

        self.anim = AnimatedEntity()
        self.anim.loadAnimation(resourceManager.getAnimFile(
            resourceManager.getAnimName(self.index)))
        self.anim.x, self.anim.y = ((game.config.windowWidth * 3 / 4) - (self.anim.width / 2),
                                    (game.config.windowHeight / 3) - (self.anim.height / 2))
        self.anim.currentClip = 'down'

        rect = pygame.Rect(0, 0, 64, 64)
        rect.center = (game.config.windowWidth * 5 /
                       8, game.config.windowHeight / 3)
        self.leftListButton = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, '<')
        self.leftListButton.onClick = self.goToLeftList

        rect.centerx = game.config.windowWidth * 7 / 8
        self.rightListButton = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, '>')
        self.rightListButton.onClick = self.goToRightList

        self.ui = self.createUI()
        self.done = False
        self.controls = [
            self.anim,
            self.leftListButton,
            self.rightListButton,
        ]

    def createUI(self):
        grid1 = GridContainer(0, 0, self.game.surface.get_width() / 3, self.game.surface.get_height())
        grid1.setGrid(2, 1)

        buttonPlay = Button(0, 0, 450, 70, self.font, 'Quiero jugar!')
        buttonPlay.onClick = self.onGoPlay
        grid1.addControl(buttonPlay, (0, 0))

        buttonQuit = Button(0, 0, 450, 70, self.font, 'Tengo miedo!, me salgo')
        buttonQuit.onClick = self.onGoQuit
        grid1.addControl(buttonQuit, (1, 0))

        box1 = BoxContainer(BoxContainer.VERTICAL, self.game.surface.get_width() / 2, 0,
                            self.game.surface.get_width() / 2, self.game.surface.get_height())

        musicButton = Button(0, 0, 256, 64, self.font, 'Music: ON')
        musicButton.onClick = self.onMusicButton
        box1.addControl(musicButton)

        soundButton = Button(0, 0, 256, 64, self.font, 'Sounds: ON')
        soundButton.onClick = self.onSoundButton
        box1.addControl(soundButton)

        label1 = Label(0, 0, 450, 70, self.font, 'Nombre del heroe:', (0, 128, 255))
        box1.addControl(label1)

        inputBox1 = InputBox(0, 0, 450, 70, self.font)
        inputBox1.name = 'playerName'
        inputBox1.onChange = self.onChangeName

        box1.addControl(inputBox1)
        # grid3 = GridContainer()
        # grid3.setGrid(1, 2)
        # grid3.addControl(grid1, (0, 0))
        # grid3.addControl(grid2, (0, 2))

        ui = Container(0, 0, self.game.surface.get_width(), self.game.surface.get_height())
        ui.addControl(grid1)
        ui.addControl(box1)
        # ui.addControl(grid3)
        return ui

    def handleEvent(self, event):
        self.ui.handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: preguntarle al usuario si esta seguro de salir
                self.game.quit()
                return

    def handleMessage(self, message):
        pass

    # def update(self, deltaTime: float):
    #     self.ui.update(deltaTime)

    def render(self, surface: pygame.Surface):
        surface.fill((30, 30, 30))
        self.ui.render(surface, self.camera)
        # TODO: si el cliente está conectado mostrar a que servidor esta conectado, sino entonces indicar que no esta conectado

    def onEnterScene(self):
        if (self.game.player is not None) and (self.game.player.name is None):
            self.game.loadSettings()
        control = self.ui.getControlByName('playerName')
        control.text = self.game.player.name

    def onGoPlay(self, sender):
        # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
        control = self.ui.getControlByName('playerName')
        self.game.player.setName(control.text)
        self.game.player.loadAnimation(
            resourceManager.getAnimFile(resourceManager.getAnimName(self.index)))
        self.game.saveSettings()
        if not self.game.client.connected:
            if not self.game.client.connect(self.game.player):
                # TODO: en vez de finaizar aqui simplemente se muestra un mensaje en pantalla indicandole al usuario que no se pudo conectar
                # TODO: un boton en la pantalla permite salir, esta linea va allá
                resourceManager.playSound('error')
                pass
        if self.game.client.connected:
            resourceManager.playSound('title')
            self.game.setScene('play')

    def onGoQuit(self, sender):
        self.game.quit()

    def goToLeftList(self, sender):
        resourceManager.playSound('select')
        self.index -= 1
        if self.index < 0:
            self.index = resourceManager.getAnimCount() - 1
        self.anim.loadAnimation(resourceManager.getAnimFile(
            resourceManager.getAnimName(self.index)))
        self.anim.currentClip = 'down'

    def goToRightList(self, sender):
        resourceManager.playSound('select')
        self.index += 1
        if self.index > (resourceManager.getAnimCount() - 1):
            self.index = 0
        self.anim.loadAnimation(resourceManager.getAnimFile(
            resourceManager.getAnimName(self.index)))
        self.anim.currentClip = 'down'

    @staticmethod
    def onChangeName(sender):
        resourceManager.playSound('hit-key')

    @staticmethod
    def onMusicButton(sender: Button):
        enable = "ON" if resourceManager.flipEnableMusic() else "OFF"
        sender.text = "Music: " + enable

    @staticmethod
    def onSoundButton(sender: Button):
        enable = "ON" if resourceManager.flipEnableSound() else "OFF"
        sender.text = "Sounds: " + enable
