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
enableMusic = None
enableSound = None
namesAnimList = ['Bob', 'Henry', 'John', 'Charly']


def init(resPathVal: str, imgsVal: {}, soundsVal: {}, fontsVal: {}, animsVal: {}, tilesetsVal: {}, mapsVal: {}):
    global resPath
    global imgs
    global sounds
    global fonts
    global anims
    global tilesets
    global maps
    global enableMusic
    global enableSound
    enableSound = True
    enableMusic = True
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


def getRandomCharAnimName():
    global namesAnimList
    return choice(namesAnimList)


def getRandomCharAnimFile():
    global namesAnimList
    return getAnimFile(getRandomCharAnimName())


def getText(text, font, col):
    surface = font.render(text, True, col)
    return surface, pygame.Rect(0, 0, surface.get_width(), surface.get_height())


def playSound(name):
    global __soundLibrary
    try:
        global enableSound
        if enableSound:
            sound = __soundLibrary.get(name)
            if sound is None:
                # canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                sound = pygame.mixer.Sound(getSoundPath(name))
                __soundLibrary[name] = sound
            sound.set_volume(0.5)
            sound.play()
    except Exception as e:
        print("😞 No se pudo cargar audio " + getSoundPath(name), e)


def playSong(name, loops=-1):
    try:
        pygame.mixer.music.load(getSoundPath(name))
        pygame.mixer.music.play(loops)
    except Exception as e:
        print("😞 No se pudo cargar audio " + getSoundPath(name), e)


def flipEnableMusic():
    global enableMusic
    enableMusic = not enableMusic
    if enableMusic:
        pygame.mixer.unpause()
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
        pygame.mixer.pause()
    return enableMusic


def flipEnableSound():
    global enableSound
    enableSound = not enableSound
    return enableSound

# def playRandomSong():
#     global __currentlySong, __songs
#     nextSong = random.choice(__songs)
#     while nextSong == __currentlySong:
#         nextSong = random.choice(__songs)
#     __currentlySong = nextSong
#     pygame.mixer.music.load(nextSong)
#     pygame.mixer.music.play()

def blitMultiLineText(surface, text, rect, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    maxWidth, maxHeight = rect.w, rect.h
    x, y = 0, 0
    for line in words:
        for word in line:
            wordSurface = font.render(word, 0, color)
            wordWidth, wordHeight = wordSurface.get_size()
            if x + wordWidth >= maxWidth:
                x = 0  # Reset the x.
                y += wordHeight  # Start on new row.
            surface.blit(wordSurface, (rect.x + x, rect.y + y))
            x += wordWidth + space
        x = 0  # Reset the x.
        y += wordHeight  # Start on n

def AAfilledRoundedRect(surface,rect,color,radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """
    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)
    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)
    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))
    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)