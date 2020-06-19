import importlib
import os
from random import choice, random

import pygame
from core import (Character, Entity, Game, Map, Path, Scene, SimpleCamera,
                  Vector2D, collisionManager, entityManager, resourceManager)
from OnlinePlayer import OnlinePlayer
from Player import Player
from ui import Button, Text


def getFirst(list, filter):
    for x in list:
        if filter(x):
            return x
    return None


def getValidRadomPos(worlRect: pygame.Rect, rect: pygame.Rect):
    while True:
        rect.x = int(random() * worlRect.w)
        rect.y = int(random() * worlRect.h)
        if not collisionManager.checkCollistion(rect):
            return rect


def locateInValidRadomPos(worlRect: pygame.Rect, entity: Entity):
    pos = getValidRadomPos(worlRect, entity.getCollisionRect())
    entity.setPos(pos.x, pos.y)


class Playground(Scene):
    player = None
    players = {}

    characters = [

    ]

    def __init__(self, game: Game, map: Map):
        super().__init__(game)
        self.map = map
        self.paused = False
        name = resourceManager.getRandomCharAnimName()
        worlRect = map.getRect()

        self.player = Player(name, name, (0, 0), (0, 24, 34, 32))
        locateInValidRadomPos(worlRect, self.player)

        collisionManager.registerMovingEntity(self.player)

        self.loadScripts(worlRect)

        # for i in range(1, 5):
        #     character = Character('Wander', res.getRandomCharAnimName(), (0, 0))
        #     locateInValidRadomPos(worlRect, character)
        #     character.steering.wanderEnabled = True
        #     self.characters.append(character)
        #     collisionManager.registerMovingEntity(character)

        # for i in range(1, 5):
        #     character = Character('Seek', res.getRandomCharAnimName(), (0, 0))
        #     locateInValidRadomPos(worlRect, character)
        #     character.steering.seekEnabled = True
        #     character.steering.seekTarget = self.player
        #     self.characters.append(character)
        #     collisionManager.registerMovingEntity(character)

        # for i in range(1, 5):
        #     name = res.getRandomCharAnimName()
        #     character = Character('Flee', res.getRandomCharAnimName(), (0, 0))
        #     locateInValidRadomPos(worlRect, character)
        #     character.steering.fleeEnabled = True
        #     character.steering.fleeTarget = self.player
        #     self.characters.append(character)
        #     collisionManager.registerMovingEntity(character)

        # for i in range(1, 5):
        #     character = Character('Arrive', res.getRandomCharAnimName(), (0, 0))
        #     locateInValidRadomPos(worlRect, character)
        #     character.steering.arriveEnabled = True
        #     character.steering.arriveTarget = self.player
        #     self.characters.append(character)
        #     collisionManager.registerMovingEntity(character)

        entityManager.registerEntities(self.characters)

        self.font = resourceManager.getFont('minecraft', 32)
        self.label = self.font.render(
            'Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))
        self.camera = SimpleCamera(game.screen.get_width(
        ), game.screen.get_height(), self.map.width, self.map.height)
        self.camera.target = self.player
        game.setPlayer(self.player)
        entityManager.registerEntity(self.player)
        self.keysPressed = {}

        rect = pygame.Rect(0, 0, 80, 80)
        self.buttonPath = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Path')
        self.buttonPath.onClick = self.onGoPath

        rect = pygame.Rect(0, 85, 80, 80)
        self.buttonText = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Text')
        self.buttonText.onClick = self.onShowText

        self.controls = [
            self.buttonPath,
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
        self.player.move(vectorMov)

    def handleMessage(self, message):
        if message.type == 'diconnected':
            self.paused = True

    def update(self, deltaTime: float):
        if not self.paused:
            self.updateOtherPlayers()
            for i in self.players.keys():
                self.players.get(i).update(deltaTime)
            for char in self.characters:
                if char.script is not None:
                    char.script.onUpdate(char)
                char.update(deltaTime)
            for obj in self.map.objects:
                obj.update(deltaTime)
            self.player.update(deltaTime)

            collisionManager.update()

            if self.player.hasChanged:
                self.player.hasChanged = False
                self.game.client.sendPlayerStatus(self.player)
            self.camera.update(deltaTime)

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        self.map.render(screen, self.camera)
        for k in self.characters:
            k.render(screen, self.camera)
        for k in self.players.values():
            k.render(screen, self.camera)

        self.player.render(screen, self.camera)
        self.camera.render(screen)

        # mostrar un mensaje para idicar que el juego esta pausado y la razon
        # if self.paused:
        #    screen.blit(self.label, (160, 80))

        # pintar el nodo mas cercano del player
        node = self.map.pointToCell(self.player.x, self.player.y)
        point = self.map.cellToPoint(node)
        pygame.draw.circle(screen, (0, 255, 0), self.camera.apply(point), 5, 3)

        for control in self.controls:
            control.render(screen, self.camera)

    def updateOtherPlayers(self):
        # que deberia ocurrir si durante el juego se desconecta?
        playersData = self.game.client.getStatus()
        if playersData is not None:
            playerKeys = self.players.keys()
            for playerKey in playersData.keys():
                if playerKey in playerKeys:
                    self.players[playerKey].setPos(playersData.get(playerKey))
                else:
                    self.players[playerKey] = OnlinePlayer(
                        playersData.get(playerKey))
            # remover los que no se actualizaron
            toDelete = set(self.players.keys()).difference(playersData.keys())
            for playerKey in toDelete:
                del self.players[playerKey]

    def onGoPath(self, sender):
        node = self.map.pointToCell(self.player.x, self.player.y)
        graphPath = self.map.graph.randomPath(node)
        realPath = Path()
        if len(graphPath) > 0:
            for node in graphPath:
                realPath.points.append(self.map.cellToPoint(node))
            self.player.steering.followPathEnabled = True
            self.player.steering.followPathTarget = realPath

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
            bubble = getFirst(self.controls, lambda x: x.id ==
                              self.buttonText.tag)
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
                    character.script.onInit(character, worlRect)
                    self.characters.append(character)
                    collisionManager.registerMovingEntity(character)
                    print('...👍')
                except Exception as e:
                    print('❌ No se pudo cargar script', e)
        print('📜 Fin carga scripts')
