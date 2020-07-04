import json
import sys
import time

import zmq

# noinspection PyUnresolvedReferences
from .Player import Player


class Server:
    def __init__(self):
        self.isRunning = False
        self.socket = None
        self.port = 5555
        self.counter = 0
        self.players = {}
        self.commands = dict(
            signIn=self.signIn,
            update=self.updatePlayer,
            act=self.returnPlayers,
            bye=self.kickOutPlayer
        )

    def listen(self):
        print('🔥 Iniciando servidor en el puerto ' + str(self.port))
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        try:
            self.socket.bind("tcp://*:" + str(self.port))
            self.isRunning = True
        except zmq.ZMQError:
            print('🙄 Hay otra aplicación que está usando el puerto ' +
                  str(self.port) + ' en esta máquina.')
            print('🤣 Tal vez estas corriendo el servidor dos veces!')
            sys.exit()

    def send(self, message):
        try:
            self.socket.send_json(message)
            return True
        except Exception as e:
            print('❌ Server.send', message, e)
        return False

    def run(self):
        self.listen()
        while self.isRunning:
            try:
                message = json.loads(self.socket.recv_json())
                senderId = message.get('id')
                if senderId is not None:
                    senderId = int(senderId)
                data = message.get('data')
                # print('📨 mensaje: ', message, data)
                self.commands.get(message.get('command'))(senderId, data)
            except KeyboardInterrupt:
                self.isRunning = False
            except Exception as e:
                print('❌ Server.run', e)
                self.isRunning = False
            time.sleep(0.02)
        print('\n🍺 Se ha cerrado el server. Ahora vamos a por una cerveza!')

    def signIn(self, senderId, playerData):
        if isinstance(playerData, dict):
            self.players[self.counter] = Player(playerData.get("name"))
            self.players[self.counter].id = self.counter
            print('🎮 Se ha conectado el jugador ' +
                  self.players[self.counter].name)
            self.send(self.players[self.counter].id)
            self.counter += 1
            self.printPlayers()
        else:
            print('❌ Falló registrando nuevo jugador por mensaje mal formado')

    def printPlayers(self):
        print('Players (' + str(len(self.players)) + ') = [ ', end='')
        for i in self.players:
            print(i, self.players.get(i).name, end=' ')
        print(']')

    def updatePlayer(self, senderId, playerData):
        if senderId is not None:
            if isinstance(playerData, dict):
                self.players.get(senderId).update(playerData)
                self.send('')
            else:
                print('❌ Falló actualizando jugador por mensaje mal formado')
        else:
            print('❌ Falló actualizando id nulo')

    def returnPlayers(self, senderId, data):
        package = {}
        for playerKey in self.players.keys():
            if playerKey == senderId:
                continue
            package[playerKey] = self.players.get(playerKey).toDict()
        self.send(package)

    def kickOutPlayer(self, senderId, data):
        print('☹️ Se ha ido el usuario (' + str(senderId) + ') ' + self.players[senderId].name)
        del self.players[senderId]
        self.send('bye bye')

# {
#    command: str,
#    id: int,
#    data: {
#      # segun el comando
#    }
