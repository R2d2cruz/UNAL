import pygame


class Colors:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    GRAY = (96, 96, 96)
    SILVER = (128, 128, 128)


def blitMultiLineText(surface, text, rect, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # v2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    maxWidth, maxHeight = rect.w, rect.h
    wordWidth, wordHeight = 0, 0
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


def getText(text, font, col):
    surface = font.render(text, True, col)
    return surface, surface.get_rect()


def getFirst(itemList: list, itemFilter):
    for x in itemList:
        if itemFilter(x):
            return x
    return None
