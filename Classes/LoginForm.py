from pgu import gui
from .GUIWrapper import GUIWrapper
from ws_events import *
import json


class LoginForm(GUIWrapper):
    size = (800, 600)
    visible = False

    def __init__(self, pos, screen, server):
        # Веб-сокет
        self.server = server
        GUIWrapper.__init__(self, pos, screen)

    def create_components(self):
        self.username_field = gui.Input()
        button_send = gui.Button('Send')
        button_send.connect(gui.CLICK, self.send_username, '')
        table = gui.Table()
        table.tr()
        table.td(gui.Label("username: "))
        table.td(self.username_field)
        table.tr()
        table.td(button_send, colspan=2)
        self.pack_manager = table

    def send_username(self, message):
        print(self.username_field.value)
        self.server.ws.send(json.dumps({"type": "auth", "data": {"username": self.username_field.value}}))
        self.visible = False

    def event(self, event):
        if event.type == WS_AUTH:
            self.visible = True
        GUIWrapper.event(self, event)
