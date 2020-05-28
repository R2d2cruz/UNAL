import pygame
from random import choice


__soundLibrary = {}

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

def playSound(name):
    global __soundLibrary
    try:
        sound = __soundLibrary.get(name)
        if sound == None:
            #canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(getSoundPath(name))
            __soundLibrary[name] = sound
        sound.set_volume(0.5)
        sound.play()
    except Exception as e:
        print("😞 No se pudo cargar audio " +res.getSoundPath(name), e)

def playSong(name, loops=-1):
    try:
        pygame.mixer.music.load(getSoundPath(name))
        pygame.mixer.music.play(loops)
    except Exception as e:
        print("😞 No se pudo cargar audio " + getSoundPath(name), e)

# def playRandomSong():
#     global __currentlySong, __songs
#     nextSong = random.choice(__songs)
#     while nextSong == __currentlySong:
#         nextSong = random.choice(__songs)
#     __currentlySong = nextSong
#     pygame.mixer.music.load(nextSong)
#     pygame.mixer.music.play()