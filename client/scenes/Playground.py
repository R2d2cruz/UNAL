import pygame
from core.Scene import Scene
from core.Map import Map
from core.Camera import Camera
from core.Game import Game
from Player import Player
from OnlinePlayer import OnlinePlayer

class Playground(Scene):

    player = None
    players = {}

    def __init__(self, game: Game, map: Map):
        super().__init__(game)
        self.map = map
        self.paused = False
        self.player = Player(game, (100, 100), '')
        game.setPlayer(self.player)
        self.font = game.res.getFont('minecraft', 32)
        self.label = self.font.render('Juego en pausa por problemas conexión. Espere un momento', True, (255, 64, 64))
        self.camera = Camera(game.screen.get_width(), game.screen.get_height())
        self.camera.target = self.player

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.setScene("main")
            else:
                self.player.move(self.KEYDOWN.get(event.key))
        elif event.type == pygame.KEYUP:
            self.player.move((self.KEYUP.get(event.key)))

    def handleMessage(self, message):
        if message == 'diconnected':
            self.paused = True

    def update(self):
        if not self.paused:
            self.collitions()
            if self.player.hasChanged:
                self.player.hasChanged = False
                self.game.client.sendPlayerStatus(self.player)
            self.updateOtherPlayers()
            for i in self.players.keys():
                self.players.get(i).update()
            for char in self.map.characters:
                char.update()
            for obj in self.map.objects:
                obj.update()
            self.player.update()
        else:
            # mostrar un mensaje para idicar que el juego esta pausado y la razon
            pass
        self.camera.update()

    def render(self, screen):
        screen.fill((0, 0, 0))

        self.map.render(screen, self.camera)
        for k in self.players.values():
            k.render(screen, self.camera)
        
        self.player.render(screen, self.camera)
        #if self.paused:
        #    screen.blit(self.label, (160, 80))
        rect = pygame.Rect(
            self.player.x + (self.player.width / 2) - (self.camera.camera.w / 2),
            self.player.y + (self.player.height / 2) - (self.camera.camera.h / 2),
            self.camera.camera.w, 
            self.camera.camera.h)
        pygame.draw.rect(screen, (255, 0, 0), self.camera.apply(rect), 1)

    def collitions(self):
        for obj in self.map.objects:
            self.player.collitions(obj.rect)
        for i in range(len(self.map.characters)):
            self.player.collitions(self.map.characters[i])
            self.map.characters[i].collitions(self.player)

    def updateOtherPlayers(self):
        playersData = self.game.client.getStatus()
        if playersData is not None:
            playerKeys = self.players.keys()
            for playerKey in playersData.keys():
                if playerKey in playerKeys:
                    self.players[playerKey].setPos(playersData.get(playerKey))
                else:
                    self.players[playerKey] = OnlinePlayer(self.game, playersData.get(playerKey))
            # remover los que no se actualizaron
            for playerKey in playerKeys:
                if playerKey not in playersData.keys():
                    del self.players[playerKey]
