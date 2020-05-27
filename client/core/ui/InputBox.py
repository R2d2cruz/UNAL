import pygame
from core.ui.Control import Control
from core.ResourceManager import getText

class InputBox(Control):

    def __init__(self, x, y, width, heigth, font, text='', foreColor = Control.WHITE):
        super().__init__(x, y, width, heigth)
        self.__surface = None
        self.__textRect = None
        self.__font = font
        self.__color = foreColor
        self.__padding = 5
        self.fixedWidth = True
        self.text = text
        self.maxWidth = 200
        self.maxLengthReached = False
        self.onEnter = None

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__surface, self.__textRect = getText(self.__text, self.__font, self.__color)
        self.__textRect.x = self.rect.x + self.__padding
        self.__textRect.y = self.rect.y + (self.rect.h - self.__surface.get_height()) / 2
        if self.fixedWidth:
            self.maxLengthReached = self.__surface.get_width() + (self.__padding * 2) > self.rect.w
        else:
            self.rect.w = max(self.maxWidth, self.__surface.get_width() + ( self.__padding * 2) )

    def update(self):
        # TODO: self.caret.update()
        pass

    def render(self, screen):
        screen.blit(self.__surface, self.__textRect)
        # TODO: self.caret.render(screen)
        pygame.draw.rect(screen, self.__color, self.rect, 2)

    def onMouseEnter(self, event):
        self.__color = self.COLOR_ACTIVE

    def onMouseLeave(self, event):
        self.__color = self.COLOR_INACTIVE

    def onKeyDown(self, event):
        if event.key == pygame.K_RETURN:
            if self.onEnter is not None:
                pass
                #self.onEnter(self)
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif not self.maxLengthReached: 
            self.text += event.unicode
            