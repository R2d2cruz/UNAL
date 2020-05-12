import zmq


class Client:

    def __init__(self, config):
        self.id = None
        self.context = None
        self.socket = None
        self.maxAttempts = config.maxAttemptsPerServer
        self.servers = []
        for server in config.servers:
            self.servers.append("tcp://" + server)

    def connect(self):
        self.context = zmq.Context()
        attempt = 0
        for server in self.servers:
            for i in range(1, self.maxAttempts + 1):
                try:
                    print('🤞 Intentando conectarse a servidor ' + server + ' (intento ' +  str(i) + ')')
                    self.socket = self.context.socket(zmq.REQ)
                    self.socket.setsockopt(zmq.SNDTIMEO, 1000)
                    self.socket.setsockopt(zmq.RCVTIMEO, 1000)
                    self.socket.setsockopt(zmq.LINGER, 1000)
                    self.socket.connect(server)
                    self.id = self.getId()
                    print('👍 Conexión exitosa. Id de cliente: ' + self.id)
                    return True
                except zmq.Again as e:
                    print('👎 Conexión fallida. Cerrando socket...')
                    self.socket.close()
                except Exception as e:
                    print('Error', e)
                    self.close()
        print("😞 No se pudo conectar. Por favor verifique que la configuración en config.json sea correcta y vuelva a intentar.")
        return False

    def send(self, message):
        try:
            self.socket.send_string(message)
        except Exception as e:
            print('❌ Client.send', message, e)

    # este no debe usar `try` para permitir generar excepcion en connect
    def getId(self):
        self.socket.send_string("createPlayer")
        return self.socket.recv_string()

    def getStatus(self):
        self.send("act_" + self.id)
        return self.read()
      
    def sendPlayerStatus(self, player):
        self.send("update_" + self.id + "_" + player.to_json())
        return self.read()

    def read(self):
        try:
            return self.socket.recv_string()
        except Exception as e:
            print('❌ Client.read', e)
            print(e)

    def close(self):
        if self.socket is not None:
            self.socket.close()
        if self.context is not None:
            self.context.term()
