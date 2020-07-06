import json

import pygame

from game.core import Colors

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

styles = [
    'fontColor',
    'minWidth',
    'minHeight'
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


class SkinElement:
    def __init__(self):
        self.styles = {}
        self.surfaces = {}


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
        self.skin[element] = SkinElement()
        elementData = data.get(element)
        sheetFile = elementData.get('sheet')
        sheet = pygame.image.load(skinPath + '/' + sheetFile)
        for zone in zones:
            box = elementData.get(zone)
            if box is not None:
                sheet.set_clip(box)
                self.skin[element].surfaces[zone] = sheet.subsurface(sheet.get_clip())
        for style in styles:
            if style is not None:
                self.skin[element].styles[style] = elementData.get(style)
        if self.skin[element].styles['minWidth'] is None:
            min = 0
            if self.skin[element].surfaces['left'] is not None:
                min += self.skin[element].surfaces['left'].get_width()
            if self.skin[element].surfaces['right'] is not None:
                min += self.skin[element].surfaces['right'].get_width()
            self.skin[element].styles['minWidth'] = min
        if self.skin[element].styles['minHeight'] is None:
            min = 0
            if self.skin[element].surfaces['top'] is not None:
                min += self.skin[element].surfaces['top'].get_width()
            if self.skin[element].surfaces['bottom'] is not None:
                min += self.skin[element].surfaces['bottom'].get_width()
            self.skin[element].styles['minHeight'] = min
        if self.skin[element].styles['fontColor'] is None:
            self.skin[element].styles['fontColor'] = Colors.BLACK


    @staticmethod
    def renderSkin(surface, rect, skin):
        center = pygame.Rect(
            rect.left + skin.surfaces['top-left'].get_width(),
            rect.top + skin.surfaces['top-left'].get_height(),
            rect.width - skin.surfaces['top-left'].get_width() - skin.surfaces['bottom-right'].get_width(),
            rect.height - skin.surfaces['top-right'].get_height() - skin.surfaces['bottom-right'].get_height()
        )
        bottomRightPos = (
            rect.right - skin.surfaces['bottom-right'].get_width(), rect.bottom - skin.surfaces['bottom-right'].get_height())
        surface.blit(skin.surfaces['top-left'], rect.topleft)
        surface.blit(skin.surfaces['top-right'], (rect.right - skin.surfaces['top-right'].get_width(), rect.top))
        surface.blit(skin.surfaces['bottom-left'], (rect.left, rect.bottom - skin.surfaces['bottom-left'].get_height()))
        surface.blit(skin.surfaces['bottom-right'], bottomRightPos)

        GUI.repeatH(surface, skin.surfaces['top'], pygame.Rect(
            center.left, rect.top, center.width, skin.surfaces['top'].get_height()))

        GUI.repeatH(surface, skin.surfaces['bottom'], pygame.Rect(
            center.left, center.bottom, center.width, skin.surfaces['top'].get_height()))

        GUI.repeatV(surface, skin.surfaces['left'], pygame.Rect(
            rect.left, center.top, skin.surfaces['left'].get_width(), center.height))

        GUI.repeatV(surface, skin.surfaces['right'], pygame.Rect(
            center.right, center.top, skin.surfaces['right'].get_width(), center.height))

        GUI.repeatHV(surface, skin.surfaces['center'], center)

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
