import pygame
from ws_events import *
import json
import websocket
import threading


class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "8888"
        self.ws = None

    def connect(self):
        # TODO: заменить адрес и порт сервера
        self.ws = websocket.WebSocketApp("ws://192.168.1.101:8888/websocket",
                                         on_data=Server.on_data, on_error=Server.on_errors)
        threading.Thread(target=self.ws.run_forever).start()

    @staticmethod
    def on_data(cls, data, opcode, fin):
        # TODO: добавить обработку ошибок при некорректной data
        data = json.loads(data)
        print("data = ", data)
        # if data.get("type") == "error":
        #     Server.on_errors(data)
        custom_event = pygame.event.Event(WS_MESSAGE, data=data, test=0)
        pygame.event.post(custom_event)

    @staticmethod
    def on_errors(cls, data):
        print("error = ", data)
        custom_event = pygame.event.Event(WS_ERROR, error=data)
        pygame.event.post(custom_event)
