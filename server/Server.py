import zmq
import json
from Player import Player

class Server:

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        self.counter = 0
        self.index = 0
        self.players = {

        }
        self.commands = {
            "createPlayer": self.createPlayer,
            "update": self.updatePlayer,
            "act": self.returnPlayers
        }

    def run(self):
        while True:
            message = self.socket.recv_string()
            try:
                self.commands.get((message.split("_"))[0])(message)
            except:
                print("error")

    def createPlayer(self, message):
        self.players[self.counter] = Player()
        self.socket.send_string(str(self.counter))
        self.counter += 1
        self.printPlayers()
        print(self.index)

    def printPlayers(self):
        print('Players (' + str(len(self.players)) + ') = [ ', end= '')
        for i in self.players:
            print(i, end= ' ')
        print(']')

    def updatePlayer(self, message):
        information = message.split("_")
        self.players.get(int(information[1])).update(information[2])
        self.socket.send_string("")

    def returnPlayers(self, message):
        information = message.split("_")
        package = {}
        for i in self.players.keys():
            if i == int(information[1]):
                continue
            package[i] = self.players.get(i).compac()
        self.socket.send_string(json.dumps(package))

# 0 = command
# 1 = id player
# 2 = {
#   "x" = x
#   "y" = y
#   "a" = action
# }