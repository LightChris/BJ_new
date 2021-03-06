import pygame
from ws_events import *
import json
import websocket
import threading
from settings import *


class Server:
    def __init__(self):
        self.ws = None

    def connect(self):
        self.ws = websocket.WebSocketApp("ws://" + HOST + ":" + PORT + "/websocket",
                                         on_data=Server.on_data, on_error=Server.on_errors)
        threading.Thread(target=self.ws.run_forever).start()

    @staticmethod
    def on_data(cls, data, opcode, fin):
        # TODO: добавить обработку ошибок при некорректной data
        data = json.loads(data)
        print("data = ", data)
        if data.get("type") == "id":
            # custom_event = pygame.event.Event(WS_YOU_ID, id=data.get('client_id'), name=data.get('username'))
            custom_event = pygame.event.Event(WS_YOU_ID, id=data.get('client_id'))
            pygame.event.post(custom_event)
            return
        custom_event = pygame.event.Event(WS_MESSAGE, data=data)
        pygame.event.post(custom_event)

    @staticmethod
    def on_errors(cls, data):
        print("error = ", data)
        custom_event = pygame.event.Event(WS_ERROR, error=data)
        pygame.event.post(custom_event)
