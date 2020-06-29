import os
from random import choice

import pygame

from game.scripts.CharacterWrapper import CharacterWrapper
from .entities import HealthPotion
from .entities.Item import Book
from ..core import (Game, TiledMap, Scene, SimpleCamera,
                    Vector2D, resourceManager, World, MovingEntity, Colors, Character)
from ..core.SelectionBox import SelectionBox
from ..net.OnlinePlayer import OnlinePlayer
from ..ui import Button, GridContainer, Container, Label


class Playground(Scene):

    def __init__(self, game: Game):
        super().__init__(game)
        self.players = {}
        self.selectionBox = SelectionBox()
        self.world = None
        self.camera = None
        self.spawningPoints = []
        self.paused = False
        self.player = None
        self.font = None

    def onEnterScene(self, data: dict = None):
        if self.ui is None:
            self.ui = self.createUI()
        self.loadWorld(data.get('mapName'), data.get('playerName'), data.get('animName'))
        self.game.client.sendPlayerStatus(self.player)

    def createUI(self):
        self.font = resourceManager.getFont('MinecraftRegular', 18)
        # self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))

        label = Label(160, 0, 100, 40, self.font, '')
        label.name = 'status'

        grid = GridContainer(0, 0, 160, self.game.surface.get_height())
        grid.setGrid(10, 1)
        buttonPath = Button(0, 0, 0, 0, self.font, 'Follow Path')
        buttonPath.onClick = self.onGoPath
        grid.addControl(buttonPath, (0, 0))

        buttonWander1 = Button(0, 0, 0, 0, self.font, 'Start Wander')
        buttonWander1.onClick = self.onStartWander
        grid.addControl(buttonWander1, (1, 0))

        buttonWander2 = Button(0, 0, 0, 0, self.font, 'Stop Wander')
        buttonWander2.onClick = self.onStopWander
        grid.addControl(buttonWander2, (2, 0))

        # buttonText = Button(0, 0, 0, 0, self.font, 'Text')
        # buttonText.onClick = self.onShowText
        # grid.addControl(buttonText, (3, 0))

        buttonRandom = Button(0, 0, 0, 0, self.font, 'Random Pos')
        buttonRandom.onClick = self.onRandomPos
        grid.addControl(buttonRandom, (3, 0))

        buttonText = Button(0, 0, 0, 0, self.font, 'Salir')
        buttonText.onClick = self.onQuit
        grid.addControl(buttonText, (9, 0))

        ui = Container(0, 0, self.game.windowWidth, self.game.windowHeight)
        ui.addControl(grid)
        ui.addControl(label)
        return ui

    def onKeyDown(self, event):
        self.evalMove()

    def onKeyUp(self, event):
        if event.key == pygame.K_ESCAPE:
            self.onQuit(None)
        elif event.key == pygame.K_f:
            self.player.dropBook()
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
        vectorMov = Vector2D()
        if self.game.keysPressed[pygame.K_RIGHT]:
            vectorMov.x = 1
        if self.game.keysPressed[pygame.K_LEFT]:
            vectorMov.x = -1
        if self.game.keysPressed[pygame.K_DOWN]:
            vectorMov.y = 1
        if self.game.keysPressed[pygame.K_UP]:
            vectorMov.y = -1
        self.player.velocity = vectorMov

    def update(self, deltaTime: float):
        if not self.paused:
            self.updateOtherPlayers(deltaTime)
            self.world.update(deltaTime)

            if self.player.hasChanged:
                self.player.hasChanged = False
                self.game.client.sendPlayerStatus(self.player)

            self.camera.update(deltaTime)

    def render(self, surface: pygame.Surface):
        surface.fill(Colors.GRAY)
        self.world.render(surface, self.camera)
        # self.camera.render(surface)

        # mostrar un mensaje para idicar que el juego esta pausado y la razon
        # if self.paused:
        #    surface.blit(self.label, (160, 80))

        # pintar el nodo mas cercano del player
        # node = self.map.pointToCell(self.player.x, self.player.y)
        # point = self.map.cellToPoint(node)
        # pygame.draw.circle(surface, (0, 255, 0), self.camera.apply(point), 5, 3)

        # pintar los vecinos mas cercanos y la grida
        # queryRadius = 75
        # queryRect = pygame.Rect(
        #     self.player.x - queryRadius,
        #     self.player.y - queryRadius,
        #     queryRadius * 2,
        #     queryRadius * 2
        # )
        # self.world.cellSpace.tagNeighborhood(self.player)
        # pygame.draw.rect(surface, (255, 255, 0), self.camera.apply(queryRect), 4)
        control = self.ui.getControlByName('status')
        if control:
            control.text = str(self.game.FPS)
        self.selectionBox.render(surface)
        self.ui.render(surface, self.camera)

    def updateOtherPlayers(self, deltaTime: float):
        # que deberia ocurrir si durante el juego se desconecta?
        playersData = self.game.client.getStatus()
        if playersData is not None:
            playerKeys = self.players.keys()
            for playerKey in playersData.keys():
                if playerKey in playerKeys:
                    self.players[playerKey].setData(playersData.get(playerKey))
                else:
                    self.players[playerKey] = OnlinePlayer(playersData.get(playerKey))
                    self.world.addEntity(self.players[playerKey])

            # remover los que no se actualizaron
            toDelete = set(self.players.keys()).difference(playersData.keys())
            for playerKey in toDelete:
                self.world.removeEntity(self.players[playerKey])
                del self.players[playerKey]

    def onGoPath(self, event, sender):
        resourceManager.playSound('select')
        if self.player.steering.followPathEnabled:
            for entity in self.selectionBox.entities:
                if issubclass(type(entity), MovingEntity):
                    entity.steering.followPathEnabled = False
                    entity.steering.followPathTarget = None
                    entity.steering.weightWander = 1.0
        else:
            for entity in self.selectionBox.entities:
                if issubclass(type(entity), MovingEntity):
                    entity.steering.weightWander = 0.001
                    self.world.followRandomPath(entity)

    def onStartWander(self, event, sender):
        resourceManager.playSound('select')
        for entity in self.selectionBox.entities:
            if issubclass(type(entity), MovingEntity):
                entity.steering.wanderEnabled = True

    def onStopWander(self, event, sender):
        resourceManager.playSound('select')
        for entity in self.selectionBox.entities:
            if issubclass(type(entity), MovingEntity):
                entity.steering.wanderEnabled = False

    def onRandomPos(self, event, sender):
        resourceManager.playSound('select')
        for entity in self.selectionBox.entities:
            if issubclass(type(entity), MovingEntity):
                self.world.locateInValidRandomPos(entity)

    # def onShowText(self, event, sender):
    #     resourceManager.playSound('select')
    #     if sender.tag is None:
    #         bubble = Text(100, 100, 800, 400, self.font, longtText)
    #         sender.tag = bubble.id
    #         self.ui.addControl(bubble)
    #     else:
    #         bubble = self.ui.getControlById(sender.tag)
    #         self.ui.removeControl(bubble)
    #         sender.tag = None

    def onQuit(self, event, sender):
        # tal vez preguntar al usuario si esta seguro
        # se guarda el juego? se cierra y libera? o se mantiene en memoria?
        self.world.clear()
        self.game.setScene("main")

    def loadWorld(self, mapName: str, playerName: str, animName: str):
        self.spawningPoints = [
            Vector2D(128, 128),
            Vector2D(192, 192),
            Vector2D(64, 64),
            Vector2D(128, 64),
            Vector2D(64, 192)
        ]
        v = 50
        worldRect = pygame.Rect(
            160,
            0,
            self.game.windowWidth - 160,
            self.game.windowHeight
        )
        self.world = World(TiledMap(mapName), worldRect)
        self.loadScripts()
        self.world.addEntity(HealthPotion('freshPotion', Vector2D(160, 288), 20))
        self.world.addEntity(Book('book', Vector2D(900, 900), dict(tittle='NN', text='', especial=None)))

        perrito = resourceManager.loadCharacter('tony', 'perrito24')
        perrito.steering.wanderEnabled = True
        perrito.maxSpeed = 0.1
        self.world.addEntity(perrito)
        self.world.locateInValidRandomPos(perrito)

        perrito = resourceManager.loadCharacter('chester', 'perrito48')
        perrito.steering.wanderEnabled = True
        perrito.maxSpeed = 0.25
        self.world.addEntity(perrito)
        self.world.locateInValidRandomPos(perrito)

        self.player = resourceManager.loadCharacter(playerName, animName)
        self.world.addEntity(self.player)
        self.world.locateInValidRandomPos(self.player)
        self.camera = SimpleCamera(
            self.world.view.width, self.world.view.height,
            self.world.rect.width, self.world.rect.height, True)
        self.camera.follow(self.player)
        self.world.createBook = self.createBook

    def loadScripts(self):
        print('📜 Cargando scripts...')
        import importlib.util
        for script in os.listdir('./scripts/characters'):
            if script.endswith(".py"):
                fileName = './scripts/characters/' + script
                moduleName = os.path.splitext(os.path.basename(script))[0].capitalize()
                try:
                    spec = importlib.util.spec_from_file_location(
                        moduleName, fileName)
                    foo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(foo)
                    character = resourceManager.loadCharacter(moduleName, 'charly')
                    character.script = foo.ScriptCharacter()
                    character.script.name = moduleName
                    spawn = choice(self.spawningPoints)
                    character.wrapper = CharacterWrapper(character, spawn)
                    self.spawningPoints.remove(spawn)
                    character.script.onInit(character.wrapper)
                    self.world.addEntity(character)
                    print('📜 script ', moduleName, '... Cargado! 👍')
                except Exception as e:
                    print('❌ No se pudo cargar script', moduleName, e)

    @staticmethod
    def createBook(name: str, position: Vector2D, data: dict, rect: tuple = (12, 12, 32, 40)):
        return Book(name, position, data, rect)
