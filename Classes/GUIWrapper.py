import pygame
from pygame import *
from pgu import gui


class GUIWrapper:
    size = (200, 200)
    visible = True

    def __init__(self, pos, screen):
        self.app = app = gui.App()
        # Область отображения объекта
        self.rect = pygame.Rect((pos, self.size))
        # Виджет для размещения компонентов
        self.pack_manager = None
        self.create_components()
        app.init(widget=self.pack_manager, screen=screen, area=self.rect)

    def create_components(self):
        # Создайте компоненты тут
        table = gui.Table()
        # Разместите компоненты на менеджере
        self.pack_manager = table

    def event(self, e):
        if not self.visible:
            return
        self.app.event(e)

    def update(self, dt):
        pass

    def render(self, screen):
        if not self.visible:
            return
        pygame.draw.rect(screen, (0, 200, 0), self.rect, 2)
        self.app.paint()
