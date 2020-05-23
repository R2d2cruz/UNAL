import pygame
from random import choice

class ResourceHandler:
    resPath = None
    imgs = None
    sounds = None
    fonts = None
    anims = None
    tilesets = None
    maps = None

    def __init__(self, resPath: str, imgs: {}, sounds: {}, fonts: {}, anims: {}, tilesets: {}, maps: {}):
        self.resPath = resPath
        self.imgs = imgs
        self.sounds = sounds
        self.fonts = fonts
        self.anims = anims
        self.tilesets = tilesets
        self.maps = maps

    def fixPath(self, filePath: str):
        return self.resPath + filePath

    def getImageFile(self, name: str):
        return self.fixPath(self.imgs.get(name))

    def getSoundPath(self, name: str):
        return self.fixPath(self.sounds.get(name))

    def getAnimFile(self, name: str):
        return self.fixPath(self.anims.get(name))

    def getFont(self, name: str, size):
        fontDef = self.fixPath(self.fonts.get(name))
        return pygame.font.Font(fontDef, size)

    def getTileset(self, name: str):
        return self.fixPath(self.tilesets.get(name))

    def getMap(self, name: str):
        return self.fixPath(self.maps.get(name))

    def loadImage(self, name: str, rect=None):
        return self.loadImageByPath(self.getImageFile(name), rect)

    def loadImageByPath(self, fileName: str, rect=None):
        image = pygame.image.load(fileName)
        if rect is not None:
            return image.subsurface(rect)
        else:
            return image
    
    def getRandomCharAnimFile(self):
        charFile = choice(('Henry', 'John', 'Charly'))
        return self.getAnimFile(charFile)