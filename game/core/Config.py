import json


class Config:
    def __init__(self, fileName: str):
        self.servers = []
        self.maxAttemptsPerServer = 0
        self.volume = 0
        self.windowWidth = 800
        self.windowHeight = 600
        self.fullScreen = False
        self.skin = None
        self.map = None
        self.load(fileName)
        if len(self.servers) == 0:
            raise Exception(
                '🙄 No se han configurado servidores en el archivo de configuracion: config.json')

    def load(self, fileName: str):
        print('⚙️ Cargando configuracion del archivo ' + fileName)
        with open(fileName) as json_file:
            data = json.load(json_file)
            for p in data['servers']:
                self.servers.append(p)
            self.maxAttemptsPerServer = data['maxAttemptsPerServer']
            self.volume = data['volume']
            self.skin = data['skin']
            self.map = data['map']
            self.windowWidth = data['windowWidth']
            self.windowHeight = data['windowHeight']
            self.fullScreen = data['fullScreen']
