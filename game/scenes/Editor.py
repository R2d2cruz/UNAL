import pygame

from .entities import HealthPotion
from ..core import (Game, TiledMap, Scene, SimpleCamera,
                    Vector2D, resourceManager, World, Colors)
from ..core.SelectionBox import SelectionBox
from ..net.OnlinePlayer import OnlinePlayer
from ..ui import Button, GridContainer, Container, BoxContainer, Image
from ..ui.ScrollBar import ScrollBar


class Editor(Scene):

    def __init__(self, game: Game):
        super().__init__(game)
        self.keysPressed = {}
        self.players = {}
        self.selectionBox = SelectionBox()
        self.world = None
        self.camera = None
        self.spawningPoints = []
        self.paused = False
        self.cross = pygame.Rect(800, 50, 32, 32)
        self.font = None
        self.ui = None
        self.vectorMov = Vector2D()

        self.scrollH = None
        self.scrollV = None

    def onEnterScene(self, data: dict = None):
        if self.ui is None:
            self.ui = self.createUI()
        self.loadWorld(data.get('mapName'))
        self.cross.center = (self.camera.view.width // 2, self.camera.view.height // 2)

        control = self.ui.getControlByName('toolBar')
        if control is not None:
            for i in range(control.rows * control.cols):
                image = Image(0, 0, 0, 0)
                image.image = self.world.map.tileset.getTileSurface(i + 1)
                control.addControl(image, (i // control.cols, i % control.cols))

        halfX = (self.world.view.width - self.cross.width) / 2
        halfY = (self.world.view.height - self.cross.height) / 2

        self.scrollH = self.ui.getControlByName('scrollHorizontal')
        self.scrollH.minValue = halfX
        self.scrollH.maxValue = self.world.rect.width - halfX
        self.scrollH.value = self.cross.centerx
        self.scrollH.step = self.scrollH.maxValue // 100  # self.world.map.tileset.tileWidth
        self.scrollH.onChange = self.onChangeScrollH

        self.scrollV = self.ui.getControlByName('scrollVertical')
        self.scrollV.minValue = halfY
        self.scrollV.maxValue = self.world.rect.height - halfY
        self.scrollV.value = self.cross.centery
        self.scrollV.step = self.scrollV.maxValue // 100  # self.world.map.tileset.tileHeight
        self.scrollV.onChange = self.onChangeScrollV

    def createUI(self):
        self.font = resourceManager.getFont('MinecraftRegular', 18)
        # self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))

        menu = BoxContainer(BoxContainer.HORIZONTAL, 0, 0, self.game.surface.get_width(), 52)

        buttonTerrain = Button(0, 0, 80, 36, self.font, 'Terreno')
        # buttonPath.onClick = self.onGoPath
        menu.addControl(buttonTerrain)

        buttonTileset = Button(0, 0, 80, 36, self.font, 'Tileset')
        # buttonPath.onClick = self.onGoPath
        menu.addControl(buttonTileset)

        buttonText = Button(0, 0, 60, 36, self.font, 'Salir')
        buttonText.onClick = self.onClickQuit
        menu.addControl(buttonText)
        ui = Container(0, 0, self.game.surface.get_width(), self.game.surface.get_height())
        ui.addControl(menu)

        tools = GridContainer(0, 52, 160, self.game.surface.get_height() - 52)
        tools.name = 'toolBar'
        tools.setGrid(20, 4)

        scrollH = ScrollBar(160, self.game.surface.get_height() - 28, self.game.surface.get_width() - 160, 28, self.font)
        scrollH.direction = ScrollBar.HORIZONTAL
        scrollH.name = 'scrollHorizontal'

        scrollV = ScrollBar(self.game.surface.get_width() - 28, 52, 28, self.game.surface.get_height() - 52 - 28, self.font)
        scrollV.direction = ScrollBar.VERTICAL
        scrollV.name = 'scrollVertical'

        ui.addControl(tools)
        ui.addControl(scrollH)
        ui.addControl(scrollV)
        return ui

    def onKeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.onQuit(None)
        else:
            self.keysPressed[event.key] = True
        self.evalMove()

    def onKeyUp(self, event):
        self.keysPressed[event.key] = False
        self.evalMove()

    def onRightMouseDown(self, event):
        # if self.world.view.collidepoint(event.pos):
        #     self.targetPos = event.pos
        pass

    def onRightMouseUp(self, event):
        if self.world.view.collidepoint(event.pos):
            pos = self.camera.unapply(event.pos)
            target = Vector2D(pos[0] - self.world.view.x, pos[1] - self.world.view.y)
            for entity in self.selectionBox.entities:
                if isinstance(entity, OnlinePlayer):
                    resourceManager.playSound('error')
                else:
                    # entity.steering.arriveEnabled = True
                    # entity.steering.arriveTarget = target
                    entity.steering.wanderEnabled = 0.0
                    self.world.followPositionPath(entity, target)

    def onLeftMouseDown(self, event):
        if self.world.view.collidepoint(event.pos):
            # resourceManager.playSound('select')
            self.selectionBox.setPointA(event.pos)

    def onLeftMouseUp(self, event):
        # if self.world.view.collidepoint(event.pos):
        if self.selectionBox.visible:
            # resourceManager.playSound('select')
            self.selectionBox.setPointB(event.pos)
            self.selectionBox.selectEntities(self.world, self.camera)

    def onMouseMove(self, event):
        if self.selectionBox.visible:
            self.selectionBox.setPointB(event.pos)

    def evalMove(self):
        self.vectorMov.setZero()
        if self.keysPressed.get(pygame.K_RIGHT):
            self.vectorMov.x = 1
        if self.keysPressed.get(pygame.K_LEFT):
            self.vectorMov.x = -1
        if self.keysPressed.get(pygame.K_DOWN):
            self.vectorMov.y = 1
        if self.keysPressed.get(pygame.K_UP):
            self.vectorMov.y = -1

    def update(self, deltaTime: float):
        step = 32
        halfX = (self.world.view.width - self.cross.width) / 2
        halfY = (self.world.view.height - self.cross.height) / 2
        offsetX = self.cross.x + max(min(self.vectorMov.x * deltaTime, step), -step)
        self.cross.x = min(self.world.rect.width - halfX, max(halfX, offsetX))
        self.scrollH.value = self.cross.centerx

        offsetY = self.cross.y + max(min(self.vectorMov.y * deltaTime, step), -step)
        self.cross.y = min(self.world.rect.height - halfY, max(halfY, offsetY))
        self.scrollV.value = self.cross.centery

        self.world.update(deltaTime)
        self.camera.update(deltaTime)

    def render(self, surface: pygame.Surface):
        surface.fill(Colors.BLACK)
        self.world.render(surface, self.camera)
        self.selectionBox.render(surface)
        self.ui.render(surface, self.camera)
        # pygame.draw.rect(surface, (255, 0, 0), self.camera.apply(self.cross), 2)

    def onClickQuit(self, event, sender):
        self.world.clear()
        self.game.quit()

    def onChangeScrollH(self, sender):
        self.cross.centerx = sender.value

    def onChangeScrollV(self, sender):
        self.cross.centery = sender.value

    def loadWorld(self, mapName: str):
        worldRect = pygame.Rect(160, 52, self.game.windowWidth - 160 - 28, self.game.windowHeight - 52 - 28)
        self.world = World(TiledMap(mapName), worldRect)
        self.world.addEntity(HealthPotion("freshPotion", Vector2D(160, 288), 20, (0, 0, 10, 12)))
        self.camera = SimpleCamera(
            self.world.view.width, self.world.view.height,
            self.world.rect.width, self.world.rect.height, True)
        self.camera.follow(self.cross)
