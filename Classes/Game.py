import os
import sys
import pygame
from pgu import gui
from pygame import *
from settings import *
from ws_events import *
from Classes.Player import *
from utilities import load_image
from Classes.Server import Server
from Classes.LoginForm import LoginForm
from Classes.ConnectForm import ConnectForm
from Classes.ButtonsForm import ButtonsForm


class Game:
    def __init__(self, server):
        pygame.init()
        self.screen = pygame.display.set_mode((RESX, RESY), 0, 32)
        pygame.display.set_caption("BlackJack v0.1.0a")
        self.run = True
        self.deck_image = load_image(path=os.path.join("images", "cards"), name="back.png")
        self.deck_pos = (600, 50)
        self.server = server

        # buttons form
        self.buttons_form = ButtonsForm((300, 550), self.screen, self.server)

        # connect form
        self.connect_form = ConnectForm((0, 0), self.screen, self.server)

        # login form
        self.login_form = LoginForm((0, 0), self.screen, self.server)

        # Список игроков
        self.players_position = [(275, 400), (25, 400), (525, 400)]
        self.current_player = None
        self.other_players = []
        self.server = Server()
        self.current_id = None

    def add_player(self, pos, id):
        player = Player(pos, id)
        self.other_players.append(player)
        return player

    def render(self, screen):
        self.connect_form.render(screen)
        self.buttons_form.render(screen)
        self.login_form.render(screen)
        if self.current_player:
            self.current_player.render(screen)
        for player in self.other_players:
            player.render(screen)
        screen.blit(self.deck_image, self.deck_pos)

    def event(self, event):
        self.buttons_form.event(event)
        self.connect_form.event(event)
        self.login_form.event(event)
        if event.type == WS_YOU_ID:
            self.current_id = event.id
            self.current_player = Player(self.players_position.pop(0), self.current_id)
        elif event.type == WS_MESSAGE:
            if event.data.get('type') == 'hit' and event.data.get('id') == self.current_id:
                card = event.data.get('card')
                print(card)
                self.current_player.add_cards(card[0], card[1])
            # if event.data.get('type') == 'hit' and event.data.get('id') % 3 == 1:
            #     card = event.data.get('card')
            #     print('card =', card)
            #     self.players[0].add_cards(card[0], card[1])
            # elif event.data.get('type') == 'hit' and event.data.get('id') % 3 == 2:
            #     card = event.data.get('card')
            #     print('card =', card)
            #     self.players[1].add_cards(card[0], card[1])
            # elif event.data.get('type') == 'hit' and event.data.get('id') % 3 == 0:
            #     card = event.data.get('card')
            #     print('card =', card)
            #     self.players[2].add_cards(card[0], card[1])
            elif event.data.get('type') == 'other_players':
                player = self.add_player(self.players_position.pop(0), event.data.get('id'))
                for card in event.data.get('hand'):
                    player.add_cards(card[1], card[0])
            elif event.data.get('type') == 'bust':
                pass
            elif event.data.get('type') == 'stand':
                pass

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    sys.exit()
                self.event(event)
            self.screen.fill((0, 100, 0))
            self.render(self.screen)
            # self.dealer.render(self.screen)

            pygame.display.flip()
