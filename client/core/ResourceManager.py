import pygame
from random import choice

resPath = None
imgs = None
sounds = None
fonts = None
anims = None
tilesets = None
maps = None


def init(resPathVal: str, imgsVal: {}, soundsVal: {}, fontsVal: {}, animsVal: {}, tilesetsVal: {}, mapsVal: {}):
    global resPath
    global imgs
    global sounds
    global fonts
    global anims
    global tilesets
    global maps
    resPath = resPathVal
    imgs = imgsVal
    sounds = soundsVal
    fonts = fontsVal
    anims = animsVal
    tilesets = tilesetsVal
    maps = mapsVal


def fixPath(filePath: str):
    return resPath + filePath


def getImageFile(name: str):
    return fixPath(imgs.get(name))


def getSoundPath(name: str):
    return fixPath(sounds.get(name))


def getAnimFile(name: str):
    return fixPath(anims.get(name))


def getFont(name: str, size):
    fontDef = fixPath(fonts.get(name))
    return pygame.font.Font(fontDef, size)


def getTileset(name: str):
    return fixPath(tilesets.get(name))


def getMap(name: str):
    return fixPath(maps.get(name))


def loadImage(name: str, rect=None):
    return loadImageByPath(getImageFile(name), rect)


def loadImageByPath(fileName: str, rect=None):
    image = pygame.image.load(fileName)
    if rect is not None:
        return image.subsurface(rect)
    else:
        return image


def getRandomCharAnimFile():
    charFile = choice(('Henry', 'John', 'Charly', 'Bob'))
    return getAnimFile(charFile)


def getText(text, font, col):
    surface = font.render(text, True, col)
    return (surface, pygame.Rect(0, 0, surface.get_width(), surface.get_height()))
