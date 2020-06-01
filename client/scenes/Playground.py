import pygame
from random import choice, random
import core.ResourceManager as res
from core.Scene import Scene
from core.Map import Map
from core.Camera import Camera
from core.Game import Game
from core.Vector2D import Vector2D
from Player import Player
from core.Character import Character
from OnlinePlayer import OnlinePlayer
from core.ui.Button import Button
from core.Path import Path

from core.CollisionManager import collisionManager


def getValidRadomPos(worlRect, rect):
    while True:
        rect.x = int(random() * worlRect.w)
        rect.y = int(random() * worlRect.h)
        if not collisionManager.checkCollistion(rect):
            return rect


def locateInValidRadomPos(worlRect, entity):
    pos = getValidRadomPos(worlRect, entity.getCollisionRect())
    entity.x = pos.x
    entity.y = pos.y


class Playground(Scene):

    player = None
    players = {}

    characters = [

    ]

    def __init__(self, game: Game, map: Map):
        super().__init__(game)
        self.map = map
        self.paused = False
        name = res.getRandomCharAnimName()
        worlRect = map.getRect()

        self.player = Player(name, name, (0, 0))
        locateInValidRadomPos(worlRect, self.player)

        collisionManager.registerMovingEntity(self.player)

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

        self.font = res.getFont('minecraft', 32)
        self.label = self.font.render(
            'Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))
        self.camera = Camera(game.screen.get_width(
        ), game.screen.get_height(), self.map.width, self.map.height)
        self.camera.target = self.player
        game.setPlayer(self.player)
        self.keysPressed = {}

        rect = pygame.Rect(0, 0, 80, 80)
        self.buttonPath = Button(
            rect.x, rect.y, rect.w, rect.h, self.font, 'Path')
        self.buttonPath.onClick = self.onGoPath

        self.controls = [
            self.buttonPath
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
        self.buttonPath.render(screen)

        # mostrar un mensaje para idicar que el juego esta pausado y la razon
        # if self.paused:
        #    screen.blit(self.label, (160, 80))

        #pintar el nodo mas cercano del player
        node = self.map.pointToCell(self.player.x, self.player.y)
        point = self.map.cellToPoint(node)
        print(self.camera.apply(point))
        pygame.draw.circle(screen, (0, 255, 0), self.camera.apply(point), 5, 3)

    def updateOtherPlayers(self):
        # que deberia ocurrir si durante el juego se desconecta?
        playersData=self.game.client.getStatus()
        if playersData is not None:
            playerKeys=self.players.keys()
            for playerKey in playersData.keys():
                if playerKey in playerKeys:
                    self.players[playerKey].setPos(playersData.get(playerKey))
                else:
                    self.players[playerKey]=OnlinePlayer(
                        playersData.get(playerKey))
            # remover los que no se actualizaron
            toDelete=set(self.players.keys()).difference(playersData.keys())
            for playerKey in toDelete:
                del self.players[playerKey]

    def onGoPath(self, sender):
        node=self.map.pointToCell(self.player.x, self.player.y)
        graphPath=self.map.graph.randomPath(node)
        realPath=Path()
        if len(graphPath) > 0:
            for node in graphPath:
                realPath.points.append(self.map.cellToPoint(node))
            self.player.steering.followPathEnabled=True
            self.player.steering.followPathTarget=realPath