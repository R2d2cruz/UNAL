import json

## esta clase es un patron, se usa para hacer que otra clase que herede de esta
## se comporte como un unico objeto en toda la aplicacion
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

## Solo debe existir un mismo config en toda la aplicacion
class Config(metaclass=Singleton):
    def __init__(self):
        self.servers = []
        self.maxAttemptsPerServer = 0
        self.load('client/config.json')
        if len(self.servers) == 0:
           raise Exception("No se han configurado servidores en el archivo de configuracion: config.json")

    def load(self, fileName):
        with open(fileName) as json_file:
            data = json.load(json_file)
            for p in data['servers']:
                self.servers.append(p["host"] + ":" + str(p["port"]))
            self.maxAttemptsPerServer = data['maxAttemptsPerServer']


