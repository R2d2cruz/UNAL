import json
import os
from random import choice

import pygame

from game.core import Character, Entity


class _ResourceManager:
    def __init__(self):
        self.__soundLibrary = {}
        self.__enableSound = True
        self.__enableMusic = True
        self.__resPath: str = ''
        self.__images = {}
        self.__sounds = {}
        self.__fonts = {}
        self.__animations = {}
        self.__tilesets = {}
        self.__maps = {}
        self.__namesAnimList = []

    def init(self, resPathVal: str, imgsVal: {}):
        self.__soundLibrary = {}
        self.__enableSound = True
        self.__enableMusic = True
        self.__resPath = resPathVal
        self.__images = imgsVal
        self.__sounds = self.loadListFromPath('sounds')
        self.__fonts = self.loadListFromPath('fonts')
        self.__animations = self.loadListFromPath('sprites')
        self.__tilesets = self.loadListFromPath('tilesets')
        self.__maps = self.loadListFromPath('maps')
        self.__namesAnimList = list(self.__animations.keys())  # <-- esto es trampa, arreglar
        self.__namesAnimList.remove("fire")

    def loadListFromPath(self, path: str):
        files = next(os.walk(self.fixPath(path)))[2]
        resources = {}
        for file in files:
            name = os.path.splitext(file)[0]
            resources[name] = os.path.join(path, file)
        return resources

    def fixPath(self, filePath: str) -> str:
        return os.path.join(self.__resPath, filePath)

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
        if self.__tilesets.get(name) is not None:
            return self.fixPath(self.__tilesets.get(name))
        raise Exception('No se encontró el tileset', name)

    def getMap(self, name: str) -> str:
        if self.__maps.get(name) is not None:
            return self.fixPath(self.__maps.get(name))
        raise Exception('No se encontró el mapa', name)

    def loadImage(self, name: str, rect=None) -> pygame.Surface:
        return self.loadImageByPath(self.getImageFile(name), rect)

    @staticmethod
    def loadImageByPath(fileName: str, rect=None) -> pygame.Surface:
        image = pygame.image.load(fileName)
        if rect is not None:
            return image.subsurface(rect)
        else:
            return image

    def getAnimName(self, index: int) -> str:
        return self.__namesAnimList[index]

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

    def loadItem(self, characterName: str) -> Entity:
        pass

    def loadCharacter(self, characterName: str, animationName: str = None) -> Character:
        character = Character((0, 0), (0, 0, 0, 0))
        character.font = resourceManager.getFont('MinecraftRegular', 14)
        character.setName(characterName)
        if animationName is None:  # esto no deberia ocurrir, arreglar!!
            animationName = resourceManager.getRandomCharAnimName()
        self.loadAnimation(character, animationName)
        character.health = 20
        return character

    def loadAnimation(self, entity, animName: str):
        fileName = self.getAnimFile(animName)
        with open(fileName) as json_file:
            data = json.load(json_file)
            entity.sheet = self.loadImageByPath(self.fixPath(data.get("image")))
            sprites = data.get("sprites")
            for key in sprites:
                entity.clips[key] = sprites[key]
            entity.width = data.get("width")
            entity.height = data.get("height")
            entity.timeStep = data.get("timeStep")
            entity.defaultClip = data.get("defaultSprite")
            if issubclass(type(entity), Character):
                entity.setCollisionRect(data.get("collisionRect"))
            entity.getNextFrame()


resourceManager = _ResourceManager()
