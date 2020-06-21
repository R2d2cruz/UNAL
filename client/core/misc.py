import pygame
from pygame.constants import BLEND_RGBA_MIN, BLEND_RGBA_MAX


def blitMultiLineText(surface, text, rect, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
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


def AAfilledRoundedRect(surface, rect, color, radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)
    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)
    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)
    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
    rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


def getText(text, font, col):
    surface = font.render(text, True, col)
    return surface, pygame.Rect(0, 0, surface.get_width(), surface.get_height())


def getFirst(itemList: list, filter):
    for x in itemList:
        if filter(x):
            return x
    return None
