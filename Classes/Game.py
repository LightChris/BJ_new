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

        # Колода
        # self.deck = Deck()

        # Диллер
        # self.dealer = Dealer((250, 110), self.deck)

        # Список игроков
        self.players_position = ((25, 400), (275, 400), (525, 400))
        self.players = []
        self.add_player(1)
        self.add_player(2)
        self.add_player(3)
        self.server = Server()

    def add_player(self, id):
        if id % 3 == 1:
            player = Player((self.players_position[0]))
        elif id % 3 == 2:
            player = Player((self.players_position[1]))
        else:
            player = Player((self.players_position[2]))
        self.players.append(player)

    def render(self, screen):
        self.connect_form.render(screen)
        self.buttons_form.render(screen)
        self.login_form.render(screen)
        screen.blit(self.deck_image, self.deck_pos)

    def event(self, event):
        self.buttons_form.event(event)
        self.connect_form.event(event)
        self.login_form.event(event)
        if event.type == WS_MESSAGE:
            if event.data.get('type') == 'hit' and event.data.get('id') % 3 == 1:
                card = event.data.get('card')
                print('card =', card)
                self.players[0].add_cards(card[0], card[1])
            elif event.data.get('type') == 'hit' and event.data.get('id') % 3 == 2:
                card = event.data.get('card')
                print('card =', card)
                self.players[1].add_cards(card[0], card[1])
            elif event.data.get('type') == 'hit' and event.data.get('id') % 3 == 0:
                card = event.data.get('card')
                print('card =', card)
                self.players[2].add_cards(card[0], card[1])
            elif event.data.get('type') == 'other_hands':
                for card in event.data.get('hand'):
                    pl_id = event.data.get('id') % 3
                    print('id =', pl_id)
                    if pl_id == 0:
                        pl_id += 3
                    print('card =', card)
                    self.players[pl_id].add_cards(card[1], card[0])
            elif event.data.get('type') == 'bust':
                pass

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    sys.exit()
                # player_id = event.data.get('id')
                # self.add_player(player_id)
                self.event(event)
            self.screen.fill((0, 100, 0))
            self.render(self.screen)
            # self.dealer.render(self.screen)
            for player in self.players:
                player.render(self.screen)
            pygame.display.flip()
