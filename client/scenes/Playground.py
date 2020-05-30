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


class Playground(Scene):

    player = None
    players = {}

    characters = [

    ]

    def __init__(self, game: Game, map: Map):
        super().__init__(game)
        self.map = map
        self.paused = False

        self.player = Player(None, choice(["Bob", "Henry"]), (100, 100))
        for i in range(1, 5):
            name = res.getRandomCharAnimName()
            x = 6 * int(random() * 10 + 1) - 3
            y = 6 * int(random() * 10 + 1) - 3
            character = Character(name, name, (32 * x, 32 * y))
            #character.steering.wanderEnabled = True
            character.steering.seekEnabled = True
            character.steering.seekTarget = self.player
            self.characters.append(character)


        self.font = res.getFont('minecraft', 32)
        self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))
        self.camera = Camera(game.screen.get_width(), game.screen.get_height(), self.map.width, self.map.height)
        self.camera.target = self.player
        game.setPlayer(self.player)
        self.keysPressed = {}

    def handleEvent(self, event):
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
            vectorMov.x += 10
        if self.keysPressed.get(pygame.K_LEFT):
            vectorMov.x -= 10
        if self.keysPressed.get(pygame.K_DOWN):
            vectorMov.y += 10
        if self.keysPressed.get(pygame.K_UP):
            vectorMov.y -= 10
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
            self.collitions()
            if self.player.hasChanged:
                self.player.hasChanged = False
                self.game.client.sendPlayerStatus(self.player)
        else:
            # mostrar un mensaje para idicar que el juego esta pausado y la razon
            pass
        self.camera.update(deltaTime)

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        self.map.render(screen, self.camera)
        for k in self.characters:
            k.render(screen, self.camera)
        for k in self.players.values():
            k.render(screen, self.camera)
        
        self.player.render(screen, self.camera)
        #if self.paused:
        #    screen.blit(self.label, (160, 80))
        self.camera.render(screen)

    def collitions(self):
        self.player.listCollitions(self.map.objects)
        for obj in self.map.objects:
            self.player.collitions(obj.rect)
        for i in range(len(self.characters)):
            self.player.collitions(self.characters[i])
            self.characters[i].collitions(self.player)

    def updateOtherPlayers(self):
        # que deberia ocurrir si durante el juego se desconecta?
        playersData = self.game.client.getStatus()
        if playersData is not None:
            playerKeys = self.players.keys()
            for playerKey in playersData.keys():
                if playerKey in playerKeys:
                    self.players[playerKey].setPos(playersData.get(playerKey))
                else:
                    self.players[playerKey] = OnlinePlayer(playersData.get(playerKey))
            # remover los que no se actualizaron
            toDelete = set(self.players.keys()).difference(playersData.keys())
            for playerKey in toDelete:
                del self.players[playerKey]
