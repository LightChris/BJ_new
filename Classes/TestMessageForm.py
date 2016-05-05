from pgu import gui
from .GUIWrapper import GUIWrapper
from ..ws_events import *
import json


class TestMessageForm(GUIWrapper):
    size = (300, 100)
    visible = True

    def __init__(self, pos, screen, ws):
        # Веб-сокет
        self.ws = ws
        GUIWrapper.__init__(self, pos, screen)

    def create_components(self):
        self.message_field = gui.TextArea()
        button_send = gui.Button('Hit')
        button_send.connect(gui.CLICK, self.send_message, '')
        table = gui.Table()
        table.tr()
        table.td(gui.Label("message: "))
        table.td(self.message_field)
        table.tr()
        table.td(button_send, colspan=2)
        self.pack_manager = table

    def send_message(self, _):
        self.ws.send(json.dumps({"type": "hit"}))

    def event(self, e):
        if e.type == WS_MESSAGE:
            print(e)
            self.message_field.value = e.data.get("message")
        GUIWrapper.event(self, e)
