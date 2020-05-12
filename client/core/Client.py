import zmq
import os

if os.name == 'nt':
    from client.core.config import Config
else:
    from Config import Config

class Client:

    def __init__(self):
        self.id = None
        self.socket = None

    def connect(self):
        config = Config()
        context = zmq.Context()
        maxAttempts = config.maxAttemptsPerServer
        attempt = 0
        for server in config.servers:
            for i in range(1, maxAttempts + 1):
              try:
                  print("Conectandose a servidor " + server + " (intento " +  str(i) + ")")
                  self.socket = context.socket(zmq.REQ)
                  self.socket.setsockopt(zmq.SNDTIMEO, 1000)
                  self.socket.setsockopt(zmq.RCVTIMEO, 1000)
                  self.socket.setsockopt(zmq.LINGER, 1000)
                  self.socket.connect("tcp://" + server)
                  self.socket.send_string("createPlayer")
                  self.id = self.socket.recv_string()
                  print("Conexión exitosa. Id de cliente: " + self.id)
                  return True
              except Exception as e:
                  print(e)
                  self.socket.close()
        print("No se pudo conectar. Por favor verifique que la configuración en config.json sea correcta y vuelva a intentar.")
        return False

    def get_id(self):
        return self.id

    def send(self, message):
        try:
            self.socket.send_string(message)
        except Exception as e:
            print(e)

    def sendId(self):
        self.send("act_" + self.id)
        return self.read()
      
    def sendPlayerStatus(self, player):
        self.send("update_" + self.id + "_" + player.to_json())
        return self.read()

    def read(self):
        try:
            return self.socket.recv_string()
        except Exception as e:
            print(e)

    def close(self):
        context.term()
