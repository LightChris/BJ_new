import os
import pygame
# from Classes.Player import *


def load_image(path, name, alpha_channel=True):
    fullname = os.path.join(path, name)  # Указываем путь к папке с картинками
    image = pygame.image.load(fullname)  # Загружаем картинку и сохраняем поверхность (Surface)
    if alpha_channel:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
