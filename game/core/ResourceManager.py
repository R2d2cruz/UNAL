from random import choice

import pygame


class _ResourceManager:
    def __init__(self):
        self.__soundLibrary = {}
        self.__enableSound = True
        self.__enableMusic = True
        self.__resPath = {}
        self.__images = {}
        self.__sounds = {}
        self.__fonts = {}
        self.__animations = {}
        self.__tilesets = {}
        self.__maps = {}
        self.__namesAnimList = []

    def init(self, resPathVal: str, imgsVal: {}, soundsVal: {}, fontsVal: {}, animsVal: {}, tilesetsVal: {},
             mapsVal: {}):
        self.__soundLibrary = {}
        self.__enableSound = True
        self.__enableMusic = True
        self.__resPath = resPathVal
        self.__images = imgsVal
        self.__sounds = soundsVal
        self.__fonts = fontsVal
        self.__animations = animsVal
        self.__tilesets = tilesetsVal
        self.__maps = mapsVal
        self.__namesAnimList = ['Bob', 'Henry', 'John', 'Charly']

    def fixPath(self, filePath: str) -> str:
        return self.__resPath + filePath

    def getImageFile(self, name: str) -> str:
        return self.fixPath(self.__images.get(name))

    def getSoundPath(self, name: str) -> str:
        return self.fixPath(self.__sounds.get(name))

    def getAnimFile(self, name: str) -> str:
        return self.fixPath(self.__animations.get(name))

    def getFont(self, name: str, size) -> pygame.font.Font:
        fontDef = self.fixPath(self.__fonts.get(name))
        return pygame.font.Font(fontDef, size)

    def getTileset(self, name: str) -> str:
        return self.fixPath(self.__tilesets.get(name))

    def getMap(self, name: str) -> str:
        return self.fixPath(self.__maps.get(name))

    def loadImage(self, name: str, rect=None) -> pygame.Surface:
        return self.loadImageByPath(self.getImageFile(name), rect)

    @staticmethod
    def loadImageByPath(fileName: str, rect=None) -> pygame.Surface:
        image = pygame.image.load(fileName)
        if rect is not None:
            return image.subsurface(rect)
        else:
            return image

    def getAnimName(self, name: str) -> str:
        return self.__namesAnimList[name]

    def getAnimCount(self):
        return len(self.__namesAnimList)

    def getRandomCharAnimName(self):
        return choice(self.__namesAnimList)

    def getRandomCharAnimFile(self):
        return self.getAnimFile(self.getRandomCharAnimName())

    def playSound(self, name: str):
        try:
            if self.__enableSound:
                sound = self.__soundLibrary.get(name)
                if sound is None:
                    # canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                    sound = pygame.mixer.Sound(self.getSoundPath(name))
                    self.__soundLibrary[name] = sound
                sound.set_volume(0.5)
                sound.play()
        except Exception as e:
            print("😞 No se pudo cargar audio " + self.getSoundPath(name), e)

    def playSong(self, name: str, loops: int = -1):
        try:
            pygame.mixer.music.load(self.getSoundPath(name))
            pygame.mixer.music.play(loops)
        except Exception as e:
            print("😞 No se pudo cargar audio " + self.getSoundPath(name), e)

    def flipEnableMusic(self):
        self.__enableMusic = not self.__enableMusic
        if self.__enableMusic:
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
            pygame.mixer.pause()
        return self.__enableMusic

    def flipEnableSound(self):
        self.__enableSound = not self.__enableSound
        return self.__enableSound

    # def playRandomSong():
    #     global __currentlySong, __songs
    #     nextSong = random.choice(__songs)
    #     while nextSong == __currentlySong:
    #         nextSong = random.choice(__songs)
    #     __currentlySong = nextSong
    #     pygame.mixer.music.load(nextSong)
    #     pygame.mixer.music.play()


resourceManager = _ResourceManager()
