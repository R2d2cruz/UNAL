import pygame
from core import AnimatedEntity, Game, NullCamera, Scene, resourceManager
from ui import Button, InputBox, Label


class MainMenu(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.camera = NullCamera()
        self.font = resourceManager.getFont('minecraft', 36)
        self.index = 0
        rect = pygame.Rect(0, 0, 450, 80)
        rect.center = (game.config.windowWidth / 4,
                       game.config.windowHeight / 3)
        self.buttonPlay = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Quiero jugar!')
        self.buttonPlay.onClick = self.onGoPlay

        rect.center = (game.config.windowWidth / 4,
                       game.config.windowHeight * 2 / 3)
        self.buttonQuit = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Tengo miedo!, me salgo')
        self.buttonQuit.onClick = self.onGoQuit

        rect.center = (game.config.windowWidth * 3 / 4, -
                       55 + game.config.windowHeight * 2 / 3)
        self.label1 = Label(rect.x, rect.y, rect.w, rect.h,
                            self.font, 'Nombre del heroe:', (0, 128, 255))

        rect.center = (game.config.windowWidth * 3 / 4,
                       game.config.windowHeight * 2 / 3)
        self.inputBox1 = InputBox(rect.x, rect.y, rect.w, rect.h, self.font)
        self.inputBox1.onChange = self.onChangeName

        self.anim = AnimatedEntity()
        self.anim.loadAnimation(resourceManager.getAnimFile(
            resourceManager.getAnimName(self.index)))
        self.anim.x, self.anim.y = ((game.config.windowWidth * 3 / 4) - (self.anim.width / 2),
                                    (game.config.windowHeight / 3) - (self.anim.height / 2))
        self.anim.currentClip = 'down'

        rect = pygame.Rect(0, 0, 256, 64)
        rect.center = (game.config.windowWidth * 7 /
                       8, game.config.windowHeight / 8)
        self.musicButton = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Music: ON')
        self.musicButton.onClick = self.onMusicButton

        rect.centerx = game.config.windowWidth * 5 / 8
        self.soundButton = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Sounds: ON')
        self.soundButton.onClick = self.onSoundButton

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

        self.done = False
        self.controls = [
            self.buttonPlay,
            self.buttonQuit,
            self.label1,
            self.inputBox1,
            self.anim,
            self.leftListButton,
            self.rightListButton,
            self.musicButton,
            self.soundButton
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

    def update(self, deltaTime: float):
        for box in self.controls:
            box.update(deltaTime)

    def render(self, screen: pygame.Surface):
        screen.fill((30, 30, 30))
        for control in self.controls:
            control.render(screen, self.camera)
        # TODO: si el cliente está conectado mostrar a que servidor esta conectado, sino entonces indicar que no esta conectado

    def onEnterScene(self):
        if (self.game.player is not None) and (self.game.player.name is None):
            self.game.loadSettings()
        self.inputBox1.text = self.game.player.name

    def onGoPlay(self, sender):
        # TODO: evaluar si se escribió un nombre valido y arrojar un error en pantalla si no
        self.game.player.setName(self.inputBox1.text)
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
