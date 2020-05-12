import json


class Config:
    def __init__(self):
        self.servers = []
        self.maxAttemptsPerServer = 0
        try:
            self.load('client/config.json')
        except FileNotFoundError:
            self.load('config.json')
        if len(self.servers) == 0:
            raise Exception('🙄 No se han configurado servidores en el archivo de configuracion: config.json')

    def load(self, fileName):
        print('⚙️ Cargando configuracion del archivo ' + fileName)
        with open(fileName) as json_file:
            data = json.load(json_file)
            for p in data['servers']:
                self.servers.append(p)
            self.maxAttemptsPerServer = data['maxAttemptsPerServer']
