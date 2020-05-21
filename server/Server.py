import zmq
import json
import sys
import os

if os.name == "nt":
    from server.Player import Player
else:
    # noinspection PyUnresolvedReferences
    from Player import Player


class Server:
    def __init__(self):
        self.isRunning = False
        self.socket = None
        self.port = 5555
        self.counter = 0
        self.players = {}
        self.commands = {
            "createPlayer": self.createPlayer,
            "update": self.updatePlayer,
            "act": self.returnPlayers
        }

    def listen(self):
        print('🔥 Iniciando servidor en el puerto ' + str(self.port))
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        try:
            self.socket.bind("tcp://*:" + str(self.port))
        except zmq.ZMQError as e:
            print('🙄 Hay otra aplicación que está usando el puerto ' + str(self.port) + ' en esta máquina.')
            print('🤣 Tal vez estas corriendo el servidor dos veces!')
            sys.exit()

    def run(self):
        self.isRunning = True
        self.listen()
        while self.isRunning:
            try:
                message = self.socket.recv_string()
                self.commands.get((message.split("_"))[0])(message) 
            except KeyboardInterrupt:
                self.isRunning = False
            except Exception as e:
                print("Error", e)
        print('\n\🍺 Se ha cerrado el server. Ahora vamos a por una cerveza!')

    def createPlayer(self, message):
        print('🎮 Se ha conectado un jugador ')
        self.players[self.counter] = Player((message.split("_"))[1])
        self.socket.send_string(str(self.counter))
        self.counter += 1
        self.printPlayers()

    def printPlayers(self):
        print('Players (' + str(len(self.players)) + ') = [ ', end= '')
        for i in self.players:
            print(i, self.players.get(i).name, end= ' ')
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
            package[i] = self.players.get(i).to_json()
        self.socket.send_string(json.dumps(package))

# 0 = command
# 1 = id player
# 2 = {
#   "x" = x
#   "y" = y
#   "a" = action
# }