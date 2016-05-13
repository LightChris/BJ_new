from pgu import gui
from .GUIWrapper import GUIWrapper
from ws_events import *
import json


class ButtonsForm(GUIWrapper):
    size = (175, 25)
    visible = False

    def __init__(self, pos, screen, server):
        # Веб-сокет
        self.server = server
        GUIWrapper.__init__(self, pos, screen)

    def create_components(self):
        hit_button = gui.Button("Hit")
        hit_button.connect(gui.CLICK, self.hit)
        stand_button = gui.Button("Stand")
        stand_button.connect(gui.CLICK, self.stand)
        table = gui.Table()
        table.td(hit_button)
        table.td(stand_button)
        self.pack_manager = table

    def hit(self):
        print("Hit!")
        self.server.ws.send(json.dumps({"type": "hit"}))

    def stand(self):
        print("Stand!")
        self.server.ws.send(json.dumps({"type": "stand"}))

    def event(self, event):
        GUIWrapper.event(self, event)
        if event.type == WS_MESSAGE:
            print("WS_MESSAGE", event.data.get("type"))
            if event.data.get("type") == 'id':
                self.visible = True
