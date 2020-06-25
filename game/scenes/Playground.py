import os
from random import choice

import pygame

from .entities import HealthPotion, Player
from ..core.CharacterWrapper import CharacterWrapper
from ..core import (Character, Game, TiledMap, Scene, SimpleCamera,
                    Vector2D, resourceManager, AnimatedEntity, World, collisionManager, entityManager, MovingEntity)
from ..net.OnlinePlayer import OnlinePlayer
from ..ui import Button, Text, GridContainer, Container

LEFT = 1
RIGHT = 3


class SelectionBox:
    def __init__(self):
        self.__pointA = None
        self.__pointB = None
        self.__entities = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.valid = False
        self.visible = False

    @property
    def entities(self):
        return self.__entities

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setPointA(self, point):
        self.clear()
        if point is not None:
            self.__pointA = point
            self.visible = True

    def setPointB(self, point):
        if point is not None:
            self.visible = True
            self.x = min(self.__pointA[0], point[0])
            self.y = min(self.__pointA[1], point[1])
            self.width = max(1, abs(self.__pointA[0] - point[0]))
            self.height = max(1, abs(self.__pointA[1] - point[1]))
            if self.width > 0 and self.height > 0:
                self.valid = True

    def clear(self):
        self.__pointA = None
        self.__pointB = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.valid = False
        self.visible = False
        for entity in self.__entities:
            entity.selected = False
        self.__entities.clear()

    def render(self, surface):
        if self.visible:
            if self.valid:
                box = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                box.fill((0, 255, 0, 128))
                pygame.draw.rect(box, pygame.Color(0, 255, 0, 255), (0, 0, self.width, self.height), 1)
                surface.blit(box, (self.x, self.y))
            else:
                pygame.draw.circle(surface, (0, 255, 0), self.__pointA, 4, 2)

    def selectEntities(self, world: World, camera: SimpleCamera):
        rect = camera.unapply(self.getRect())
        rect.x -= world.view.x
        rect.y -= world.view.y
        self.visible = False
        for entity in self.__entities:
            entity.selected = False
        self.__entities = collisionManager.queryObjects(rect, world.cellSpace)
        for entity in self.__entities:
            entity.selected = True


class Playground(Scene):

    def __init__(self, game: Game, tiledMap: TiledMap):
        super().__init__(game)
        self.keysPressed = {}
        self.players = {}
        self.selectionBox = SelectionBox()
        self.world = World(tiledMap,
                           pygame.Rect(160, 0, self.game.surface.get_width() - 160, self.game.surface.get_height()))
        self.spawningPoints = [
            Vector2D(128, 128), Vector2D(192, 192), Vector2D(64, 64), Vector2D(128, 64), Vector2D(64, 192)]

        name = resourceManager.getRandomCharAnimName()
        self.player = Player(name, name, (0, 0), (0, 24, 34, 32))
        self.world.addEntity(self.player)
        self.world.locateInValidRandomPos(self.player)
        game.setPlayer(self.player)

        self.camera = SimpleCamera(
            self.world.view.width, self.world.view.height,
            self.world.rect.width, self.world.rect.height)
        self.camera.follow(self.player)
        self.paused = False
        self.loadScripts(self.world.rect)
        self.world.addEntity(HealthPotion("freshPotion", (3, 2, 10, 12), Vector2D(160, 288), 20))

        for i in range(1, 10):
            fire = AnimatedEntity()
            fire.loadAnimation(resourceManager.getAnimFile("fire"))
            fire.x = 50 * i
            fire.y = 0
            self.world.addEntity(fire, False)

        self.font = resourceManager.getFont('minecraft', 18)
        # self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))
        self.ui = self.createUI()

    def createUI(self):
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

        buttonText = Button(0, 0, 0, 0, self.font, 'Text')
        buttonText.onClick = self.onShowText
        grid.addControl(buttonText, (3, 0))

        buttonText = Button(0, 0, 0, 0, self.font, 'Salir')
        buttonText.onClick = self.onQuit
        grid.addControl(buttonText, (9, 0))
        ui = Container(0, 0, self.game.surface.get_width(), self.game.surface.get_height())
        ui.addControl(grid)
        return ui

    def handleEvent(self, event):
        self.ui.handleEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == RIGHT:
                self.onRightMouseDown(event)
            else:
                self.onLeftMouseDown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == RIGHT:
                self.onRightMouseUp(event)
            else:
                self.onLeftMouseUp(event)
        elif event.type == pygame.MOUSEMOTION:
            if self.selectionBox.visible:
                self.selectionBox.setPointB(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.onQuit(None)
            else:
                self.keysPressed[event.key] = True
        elif event.type == pygame.KEYUP:
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
                    entity.steering.arriveEnabled = True
                    entity.steering.arriveTarget = target

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

    def evalMove(self):
        vectorMov = Vector2D()
        if self.keysPressed.get(pygame.K_RIGHT):
            vectorMov.x += 1
        if self.keysPressed.get(pygame.K_LEFT):
            vectorMov.x -= 1
        if self.keysPressed.get(pygame.K_DOWN):
            vectorMov.y += 1
        if self.keysPressed.get(pygame.K_UP):
            vectorMov.y -= 1
        self.player.velocity = vectorMov

    def handleMessage(self, message):
        if message.type == 'diconnected':
            self.paused = True

    def update(self, deltaTime: float):
        if not self.paused:
            self.updateOtherPlayers(deltaTime)
            self.world.update(deltaTime)

            if self.player.hasChanged:
                self.player.hasChanged = False
                self.game.client.sendPlayerStatus(self.player)

            self.camera.update(deltaTime)

    def render(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
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
        # self.cellSpace.tagNeighborhood(self.player, queryRadius)
        # pygame.draw.rect(surface, (255, 255, 0), self.camera.apply(queryRect), 4)
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

    def onGoPath(self, sender):
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
                    entity.steering.weightWander = 0.1
                    self.world.followRandomPath(entity)

    def onStartWander(self, sender):
        resourceManager.playSound('select')
        for entity in self.selectionBox.entities:
            if issubclass(type(entity), MovingEntity):
                entity.steering.wanderEnabled = True

    def onStopWander(self, sender):
        resourceManager.playSound('select')
        for entity in self.selectionBox.entities:
            if issubclass(type(entity), MovingEntity):
                entity.steering.wanderEnabled = False

    def onShowText(self, sender):
        resourceManager.playSound('select')
        if sender.tag is None:
            bubble = Text(100, 100, 800, 400, self.font, longtText)
            sender.tag = bubble.id
            self.ui.addControl(bubble)
        else:
            bubble = self.ui.getControlById(sender.tag)
            self.ui.removeControl(bubble)
            sender.tag = None

    def onQuit(self, sender):
        # tal vez preguntar al usuario si esta seguro
        # se guarda el juego? se cierra y libera todo? o se mantiene en memoria?
        self.game.setScene("main")

    def loadScripts(self, worlRect):
        print('📜 Inicio carga scripts')
        import importlib.util
        for script in os.listdir('./scripts/characters'):
            if script.endswith(".py"):
                fileName = './scripts/characters/' + script
                moduleName = os.path.splitext(os.path.basename(script))[0].capitalize()
                try:
                    print('📜 Cargando script ', moduleName, end='')
                    spec = importlib.util.spec_from_file_location(
                        moduleName, fileName)
                    foo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(foo)
                    character = Character(moduleName, 'Charly', (0, 0), (0, 24, 34, 32))
                    character.script = foo.ScriptCharacter()
                    character.script.name = moduleName
                    spawn = choice(self.spawningPoints)
                    character.wrapper = CharacterWrapper(character, spawn)
                    self.spawningPoints.remove(spawn)
                    character.script.onInit(character.wrapper)
                    self.world.addEntity(character)
                    print('...👍')
                except Exception as e:
                    print('❌ No se pudo cargar script', e)
        print('📜 Fin carga scripts')


longtText = (
    "Ricardo recibió un loro por su cumpleaños; ya era un loro adulto, con una muy mala actitud y vocabulario. Cada "
    "palabra que decía estaba adornada por alguna palabrota, así como siempre, de muy mal genio. Ricardo trató, "
    "desde el primer día, de corregir la actitud del loro, diciéndole palabras bondadosas y con mucha educación, "
    "le ponía música suave y siempre lo trataba con mucho cariño.\n "
    "Llego un día en que Ricardo perdió la paciencia y gritó al loro, el cual se puso más grosero aún, hasta que en "
    "un momento de desesperación, Ricardo puso al loro en el congelador.\n "
    "Por un par de minutos aún pudo escuchar los gritos del loro y el revuelo que causaba en el compartimento, "
    "hasta que de pronto, todo fue silencio.\n "
    "Luego de un rato, Ricardo arrepentido y temeroso de haber matado al loro, rápidamente abrió la puerta del "
    "congelador.\n "
    "El loro salió y con mucha calma dio un paso al hombro de Ricardo y dijo:\n"
    "- \"Siento mucho haberte ofendido con mi lenguaje y actitud, te pido me disculpes y te prometo que en el futuro "
    "vigilaré mucho mi comportamiento\".\n "
    "Ricardo estaba muy sorprendido del tremendo cambio en la actitud del loro y estaba a punto de preguntarle qué es "
    "lo que lo había hecho cambiar de esa manera, cuando el loro continuó:\n "
    "- ¿te puedo preguntar una cosa?...\n"
    "- Si.. como no!!, -contestó Ricardo\n"
    "- ¿Qué fue lo que hizo el pollo?")
