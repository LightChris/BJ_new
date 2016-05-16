import pygame
from pgu import gui
from .GUIWrapper import GUIWrapper
from ws_events import *


class ConnectForm(GUIWrapper):
    visible = True
    size = (800, 600)

    def __init__(self, pos, screen, server):
        # Веб-сокет
        self.server = server
        self.info_text = gui.Label(".....................................")
        GUIWrapper.__init__(self, pos, screen)

    def create_components(self):
        self.info_text.style.width = 200
        self.info_text.style.height = 400
        button_connect = gui.Button('Connect')
        button_connect.connect(gui.CLICK, self.connect, '')
        table = gui.Table()
        table.tr()
        table.td(self.info_text)
        table.tr()
        table.td(button_connect)
        table.style.align = -1
        table.style.valign = -1
        self.pack_manager = table

    def connect(self, message):
        self.server.connect()

    def event(self, event):
        # print(event.type)
        if event.type == WS_ERROR:
            print("WS_ERROR", event.error)
            self.info_text.value = "Server is not available"
        if event.type == WS_MESSAGE:
            # print("WS_MESSAGE", event.data.get("type"))
            if event.data.get("type") == 'auth':
                print("Авторизация.")
                custom_event = pygame.event.Event(WS_AUTH)
                pygame.event.post(custom_event)
                self.visible = False
        GUIWrapper.event(self, event)
