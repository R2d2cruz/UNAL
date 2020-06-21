import os
from random import random

import pygame

from ..OnlinePlayer import OnlinePlayer
from ..core import (Character, Entity, Game, Path, Scene, SimpleCamera,
                    SpacePartition, Vector2D, collisionManager, resourceManager)
from ..ui import Button, Text
from ..core.misc import getFirst


class Physics(Scene):

    def __init__(self, game: Game):
        super().__init__(game)
        self.entity = []
        worlRect = pygame.Rect(0, 0, 1000, 1000)
        self.cellSpace = SpacePartition(worlRect.w, worlRect.h, int(worlRect.w / 100), int(worlRect.h / 100))

        self.camera = SimpleCamera(game.screen.get_width(), game.screen.get_height(), worlRect.w, worlRect.h)
        self.camera.target = self.camera
        game.setPlayer(self.camera)
        self.keysPressed = {}

        self.font = resourceManager.getFont('minecraft', 24)
        self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))

        rect = pygame.Rect(0, 0, 140, 50)
        self.buttonPath = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Follow Path')
        self.buttonPath.onClick = self.onGoPath

        rect = pygame.Rect(0, 55, 140, 50)
        self.buttonWander = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Wander')
        self.buttonWander.onClick = self.onGoWander

        rect = pygame.Rect(0, 110, 140, 50)
        self.buttonText = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Text')
        self.buttonText.onClick = self.onShowText

        self.controls = [
            self.buttonPath,
            self.buttonWander,
            self.buttonText,
        ]

    def handleEvent(self, event):
        for box in self.controls:
            box.handleEvent(event)
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
        self.camera.move(vectorMov)

    def handleMessage(self, message):
        if message.type == 'diconnected':
            self.paused = True

    def update(self, deltaTime: float):
        if not self.paused:
            for entity in self.entities:
                entity.update(deltaTime)

            self.player.update(deltaTime)
            collisionManager.update(self.cellSpace)
            self.camera.update(deltaTime)

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        self.map.render(screen, self.camera)
        for entity in self.entities:
            entity.render(screen, self.camera)

        self.player.render(screen, self.camera)
        # self.camera.render(screen)

        # mostrar un mensaje para idicar que el juego esta pausado y la razon
        # if self.paused:
        #    screen.blit(self.label, (160, 80))

        # pintar el nodo mas cercano del player
        # node = self.map.pointToCell(self.player.x, self.player.y)
        # point = self.map.cellToPoint(node)
        # pygame.draw.circle(screen, (0, 255, 0), self.camera.apply(point), 5, 3)

        # pintar los vecinos mas cercanos y la grida
        # queryRadius = 75
        # queryRect = pygame.Rect(
        #     self.player.x - queryRadius,
        #     self.player.y - queryRadius,
        #     queryRadius * 2,
        #     queryRadius * 2
        # )
        # self.cellSpace.tagNeighborhood(self.player, queryRadius)
        # pygame.draw.rect(screen, (255, 255, 0), self.camera.apply(queryRect), 4)
        # self.cellSpace.render(screen, self.camera)

        for control in self.controls:
            control.render(screen, self.camera)

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
                    self.cellSpace.registerEntity(self.players[playerKey])

            # remover los que no se actualizaron
            toDelete = set(self.players.keys()).difference(playersData.keys())
            for playerKey in toDelete:
                self.cellSpace.unregisterEntity(self.players[playerKey])
                del self.players[playerKey]

        for playerKey in self.players.keys():
            self.players[playerKey].update(deltaTime)
            self.cellSpace.updateEntity(self.players[playerKey])

    def onGoPath(self, sender):
        if self.player.steering.followPathEnabled:
            sender.backColor = (128, 128, 128)
            self.player.steering.followPathEnabled = False
            self.player.steering.followPathTarget = None
            self.player.steering.weightWander = 1.0
        else:
            self.player.steering.weightWander = 0.1
            sender.backColor = (255, 64, 64)
            self.followRandomPath(self.player)

    def onGoWander(self, sender):
        if self.player.steering.wanderEnabled:
            sender.backColor = (128, 128, 128)
            self.player.steering.wanderEnabled = False
        else:
            sender.backColor = (255, 64, 64)
            self.player.steering.wanderEnabled = True

    def onShowText(self, sender):
        if self.buttonText.tag is None:
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
            self.buttonText.tag = bubble.id
            self.controls.append(bubble)
        else:
            bubble = getFirst(self.controls, lambda x: x.id == self.buttonText.tag)
            self.controls.remove(bubble)
            self.buttonText.tag = None

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
                    self.characters.append(character)
                    collisionManager.registerMovingEntity(character)
                    self.cellSpace.registerEntity(character)
                    print('...👍')
                except Exception as e:
                    print('❌ No se pudo cargar script', e)
        print('📜 Fin carga scripts')

    def getValidRadomPos(self, worlRect: pygame.Rect, rect: pygame.Rect):
        while True:
            rect.x = int(random() * worlRect.w)
            rect.y = int(random() * worlRect.h)
            if not collisionManager.checkCollistion(rect, self.cellSpace):
                return rect

    def locateInValidRadomPos(self, worlRect: pygame.Rect, entity: Entity):
        pos = self.getValidRadomPos(worlRect, entity.getCollisionRect())
        entity.setPos(pos.x, pos.y)

    def followRandomPath(self, entity):
        node = self.map.pointToCell(entity.x, entity.y)
        graphPath = self.graph.randomPath(node)
        realPath = Path()
        if len(graphPath) > 0:
            for node in graphPath:
                realPath.points.append(self.map.cellToPoint(node))
            entity.steering.followPathEnabled = True
            entity.steering.followPathTarget = realPath
