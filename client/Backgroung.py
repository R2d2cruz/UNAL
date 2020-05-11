from OnlinePlayers import OnlinePlayer
import json


class Background:
    map = [

    ]
    frames = {

    }

    jumpPoints = [

    ]

    objects = [

    ]

    characters = [

    ]

    player = None
    players = {}
    x = 0
    y = 0
    rect = 32

    def __init__(self, game):
        self.game = game

    def changeCoord(self, x, y):
        self.x = x
        self.y = y
        for i in self.characters:
            i.change_reference_point([self.x, self.y])
        for i in self.objects:
            i.change_reference_point([self.x, self.y])
        for i in self.players.keys():
            self.players[i].change_reference_point([self.x, self.y])

    def handleEvents(self, event):
        self.player.handle_event(event)

    def updateOtherPlayers(self):
        self.game.socket.send_string("act_" + self.game.get_id())
        message = self.game.socket.recv_string()
        information = json.loads(message)
        print(information)
        keys = self.players.keys()
        for i in information.keys():
            if i in keys:
                player = self.players.get(i)
                player.update(information.get(i))
                self.players[i] = player
            else:
                self.players[i] = OnlinePlayer(information.get(i))

    def update(self):
        self.collitions()
        if self.player.get_actualizate():
            message = "update_" + self.game.get_id() + "_" + self.player.get_compac()
            try:
                self.game.socket.send_string(message)
                print(self.game.socket.recv_string())
            except:
                pass
        self.updateOtherPlayers()
        for i in self.characters:
            i.update()
            i.act()
        for i in self.objects:
            self.player.collitions(i)
        if not self.player.act():
            self.changeCoord(self.player.get_x(), self.player.get_y())
        ##print(self.y, self.player.rect.topleft[1])

    def blit(self, screen):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                screen.blit(self.frames.get(self.map[i][j]), (self.x + (self.rect * j), self.y + (self.rect * i)))
        for k in self.characters:
            k.blit(screen)
        for k in self.objects:
            k.blit(screen)
        for k in self.players.values():
            k.blit(screen)
        self.player.blit(screen)

    def collitions(self):
        for i in range(len(self.characters)):
            self.player.collitions(self.characters[i])
            self.characters[i].collitions(self.player)
