import os

import pygame

from .entities import HealthPotion, Player
from ..core import (Character, Game, TiledMap, Scene, SimpleCamera,
                    Vector2D, resourceManager, AnimatedEntity, World)
from ..net.OnlinePlayer import OnlinePlayer
from ..ui import Button, Text, GridContainer, Container


class Playground(Scene):

    def __init__(self, game: Game, tiledMap: TiledMap):
        super().__init__(game)
        self.keysPressed = {}
        self.players = {}
        self.world = World(tiledMap, pygame.Rect(160, 0, self.game.surface.get_width() - 160, self.game.surface.get_height()))

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

        self.font = resourceManager.getFont('minecraft', 24)
        # self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))
        self.ui = self.createUI()

    def createUI(self):
        grid = GridContainer(0, 0, 160, self.game.surface.get_height())
        grid.setGrid(10, 1)
        buttonPath = Button(0, 0, 0, 0, self.font, 'Follow Path')
        buttonPath.onClick = self.onGoPath
        grid.addControl(buttonPath, (0, 0))
        buttonWander = Button(0, 0, 0, 0, self.font, 'Wander')
        buttonWander.onClick = self.onGoWander
        grid.addControl(buttonWander, (1, 0))
        buttonText = Button(0, 0, 0, 0, self.font, 'Text')
        buttonText.onClick = self.onShowText
        grid.addControl(buttonText, (2, 0))
        ui = Container(0, 0, self.game.surface.get_width(), self.game.surface.get_height())
        ui.addControl(grid)
        return ui

    def handleEvent(self, event):
        self.ui.handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.setScene("main")
            else:
                self.keysPressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.keysPressed[event.key] = False
        self.evalMove()

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
        # self.cellSpace.render(surface, self.camera)

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
        if self.player.steering.followPathEnabled:
            sender.backColor = (128, 128, 128)
            self.player.steering.followPathEnabled = False
            self.player.steering.followPathTarget = None
            self.player.steering.weightWander = 1.0
        else:
            self.player.steering.weightWander = 0.1
            sender.backColor = (255, 64, 64)
            self.world.followRandomPath(self.player)

    def onGoWander(self, sender):
        if self.player.steering.wanderEnabled:
            sender.backColor = (128, 128, 128)
            self.player.steering.wanderEnabled = False
        else:
            sender.backColor = (255, 64, 64)
            self.player.steering.wanderEnabled = True

    def onShowText(self, sender):
        if sender.tag is None:
            longtText = """Ricardo recibió un loro por su cumpleaños; ya era un loro adulto, con una muy mala actitud y vocabulario. Cada palabra que decía estaba adornada por alguna palabrota, así como siempre, de muy mal genio. Ricardo trató, desde el primer día, de corregir la actitud del loro, diciéndole palabras bondadosas y con mucha educación, le ponía música suave y siempre lo trataba con mucho cariño.
    Llego un día en que Ricardo perdió la paciencia y gritó al loro, el cual se puso más grosero aún, hasta que en un momento de desesperación, Ricardo puso al loro en el congelador.
    Por un par de minutos aún pudo escuchar los gritos del loro y el revuelo que causaba en el compartimento, hasta que de pronto, todo fue silencio.
    Luego de un rato, Ricardo arrepentido y temeroso de haber matado al loro, rápidamente abrió la puerta del congelador.
    El loro salió y con mucha calma dio un paso al hombro de Ricardo y dijo:
    - "Siento mucho haberte ofendido con mi lenguaje y actitud, te pido me disculpes y te prometo que en el futuro vigilaré mucho mi comportamiento".
    Ricardo estaba muy sorprendido del tremendo cambio en la actitud del loro y estaba a punto de preguntarle qué es lo que lo había hecho cambiar de esa manera, cuando el loro continuó:
    - ¿te puedo preguntar una cosa?...
    - Si.. como no!!, -contestó Ricardo
    - ¿Qué fue lo que hizo el pollo?"""
            bubble = Text(100, 100, 800, 400, self.font, longtText)
            sender.tag = bubble.id
            self.ui.addControl(bubble)
        else:
            bubble = self.ui.getControlById(sender.tag)
            self.ui.removeControl(bubble)
            sender.tag = None

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
                    character.script.onInit(character)
                    self.world.addEntity(character)
                    print('...👍')
                except Exception as e:
                    print('❌ No se pudo cargar script', e)
        print('📜 Fin carga scripts')
