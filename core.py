import os
import pygame

def get_unused_png_name():
    fname = 1
    while os.path.isfile(str(fname) + '.png'):
        fname += 1
    return str(fname) + '.png'

def save_screen(screen):
    pygame.image.save(screen, get_unused_png_name())