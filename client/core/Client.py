import zmq
import json

class Client:

    def __init__(self, config):
        self.id = None
        self.context = None
        self.socket = None
        self.connected = False
        self.maxAttempts = config.maxAttemptsPerServer
        self.servers = []
        for server in config.servers:
            self.servers.append("tcp://" + server)

    def connect(self, name: str):
        self.context = zmq.Context()
        for server in self.servers:
            for i in range(1, self.maxAttempts + 1):
                try:
                    print('🤞 Intentando conectarse a servidor ' +
                          server + ' (intento ' + str(i) + ')')
                    self.socket = self.context.socket(zmq.REQ)
                    self.socket.setsockopt(zmq.SNDTIMEO, 1000)
                    self.socket.setsockopt(zmq.RCVTIMEO, 1000)
                    self.socket.setsockopt(zmq.LINGER, 1000)
                    self.socket.connect(server)
                    self.id = self.getId(name)
                    self.connected = True
                    print('👍 Conexión exitosa. Id de cliente: ' + str(self.id))
                    return True
                except zmq.Again as e:
                    print('👎 Conexión fallida. Cerrando socket...')
                    self.socket.close()
                except Exception as e:
                    print('❌ Client.connect', e)
                    self.close()
        print("😞 No se pudo conectar. Por favor verifique que la configuración en config.json sea correcta y vuelva a intentar.")
        return False

    def send(self, message: object):
        try:
            self.socket.send_json(message)
            return True
        except Exception as e:
            print('❌ Client.send', message, e)
            self.close()
        return False

    def read(self):
        try:
            return self.socket.recv_string()
        except Exception as e:
            self.close()
            print('❌ Client.read', e)
    
    def sendDict(self, data, ignoreState = False):
        try:
            if not ignoreState and not self.connected:
                print('❌ No se ha conectado al servidor. No se puede enviar mensaje')
                return
            if self.send(json.dumps(data)):
                response = self.read()
                return json.loads(response)
        except Exception as e:
            print('❌ Client.sendDict', e)
        return None

    # este no debe usar `try` para permitir generar excepcion en connect
    def getId(self, name):
        id = self.sendDict(dict(
            command = 'createPlayer',
            data = name
        ), True)
        if id is None:
            print('👎 ID nulo')
        return id

    def getStatus(self):
        return self.sendDict(dict(
            command = 'act',
            id = self.id
        ))

    def sendPlayerStatus(self, player):
        return self.sendDict(dict(
            command = 'update',
            id = self.id,
            data = player.toDict()
        ))

    def goodBye(self):
        print('😥 cerrando conexión con el servidor!')
        return self.sendDict(dict(
            command = 'bye',
            id = self.id
        ))

    def close(self):
        self.connected = False
        if self.socket is not None:
            self.goodBye()
            self.socket.close()
        if self.context is not None:
            self.context.term()
