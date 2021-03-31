import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey((255, 255, 255))
        if colorkey == 1:
            image.set_colorkey((0, 0, 0))
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()
