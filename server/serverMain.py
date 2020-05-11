import zmq
import json


class player:

    prevx = 0
    prevy = 0
    prevMovement = "std"
    x = 0
    y = 0
    movement = "std"

# movements:
# std = stand down
# stu = stand up
# str = stand right
# stl = stand left
# wld = walk down
# wlu = walk up
# wll = walk left
# wlr = walk right

    def update(self, information):
        message = json.loads(information)
        self.x = message.get("x")
        self.y = message.get("y")
        self.movement = message.get("a")

    def compac(self):
        return {
            "x": self.x,
            "y": self.y,
            "a": self.movement
        }


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

    def render(self):
        while True:
            message = self.socket.recv_string()

            try:
                self.commands.get((message.split("_"))[0])(message)
            except:
                print("error")

    def createPlayer(self, message):
        self.players[self.counter] = player()
        self.socket.send_string(str(self.counter))
        self.counter += 1
        for i in self.players:
            print(i)
        print(self.index)
        print(len(self.players))

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

server = Server()
server.render()
