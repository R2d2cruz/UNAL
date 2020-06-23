import json

import pygame

zones = [
    'top-left',
    'top-right',
    'bottom-left',
    'bottom-right',
    'left',
    'right',
    'top',
    'bottom',
    'center'
]

elementNames = [
    'button',
    'button-pressed',
    'button-active',
    'button-disabled',
    'panel',
    'input',
    'input-active',
    'input-disabled'
]


class GUI:
    def __init__(self):
        self.skin = {}

    def renderElement(self, surface, rect, element):
        if element in self.skin:
            GUI.renderSkin(surface, rect, self.skin[element])
        else:
            print('Element', element, 'not present in skin')

    def loadSkin(self, skinPath: str):
        with open(skinPath + '/skin.json') as jsonFile:
            data = json.load(jsonFile)
            for name in elementNames:
                self.loadSkinElement(data, name, skinPath)

    def loadSkinElement(self, data, element, skinPath):
        self.skin[element] = {}
        elementData = data.get(element)
        sheetFile = elementData.get('sheet')
        sheet = pygame.image.load(skinPath + '/' + sheetFile)
        for zone in zones:
            box = elementData.get(zone)
            sheet.set_clip(box)
            self.skin[element][zone] = sheet.subsurface(sheet.get_clip())

    @staticmethod
    def renderSkin(surface, rect, skin):
        center = pygame.Rect(
            rect.left + skin['top-left'].get_width(),
            rect.top + skin['top-left'].get_height(),
            rect.width - skin['top-left'].get_width() - skin['bottom-right'].get_width(),
            rect.height - skin['top-right'].get_height() - skin['bottom-right'].get_height()
        )
        bottomRightPos = (
        rect.right - skin['bottom-right'].get_width(), rect.bottom - skin['bottom-right'].get_height())
        surface.blit(skin['top-left'], rect.topleft)
        surface.blit(skin['top-right'], (rect.right - skin['top-right'].get_width(), rect.top))
        surface.blit(skin['bottom-left'], (rect.left, rect.bottom - skin['bottom-left'].get_height()))
        surface.blit(skin['bottom-right'], bottomRightPos)

        GUI.repeatH(surface, skin['top'], pygame.Rect(
            center.left, rect.top, center.width, skin['top'].get_height()))

        GUI.repeatH(surface, skin['bottom'], pygame.Rect(
            center.left, center.bottom, center.width, skin['top'].get_height()))

        GUI.repeatV(surface, skin['left'], pygame.Rect(
            rect.left, center.top, skin['left'].get_width(), center.height))

        GUI.repeatV(surface, skin['right'], pygame.Rect(
            center.right, center.top, skin['right'].get_width(), center.height))

        GUI.repeatHV(surface, skin['center'], center)

    @staticmethod
    def repeatH(surface, source, destRect):
        if destRect.width > 0:
            surface.set_clip(destRect)
            for i in range(destRect.width // source.get_width() + 1):
                surface.blit(source, (destRect.x + i * source.get_width(), destRect.y))
            surface.set_clip()

    @staticmethod
    def repeatV(surface, source, destRect):
        if destRect.height > 0:
            surface.set_clip(destRect)
            for i in range(destRect.height // source.get_height() + 1):
                surface.blit(source, (destRect.x, destRect.y + i * source.get_height()))
            surface.set_clip()

    @staticmethod
    def repeatHV(surface, source, destRect):
        if destRect.height > 0:
            surface.set_clip(destRect)
            for i in range(destRect.width // source.get_width() + 1):
                for j in range(destRect.height // source.get_height() + 1):
                    surface.blit(source, (destRect.x + i * source.get_width(), destRect.y + j * source.get_height()))
            surface.set_clip()


gui = GUI()
