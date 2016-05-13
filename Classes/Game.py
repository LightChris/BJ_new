import os
import sys
import pygame
from pgu import gui
from pygame import *
from settings import *
from ws_events import *
from Classes.Dealer import *
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
        self.deck = Deck()

        # Диллер
        self.dealer = Dealer((250, 110), self.deck)

        # Список игроков
        self.players_position = ((25, 400), (275, 400), (525, 400))
        self.players = []
        self.add_player(1)
        self.add_player(2)
        self.add_player(3)
        self.server = Server()

    def add_player(self, id):
        player = Player((self.players_position[id-1]), self.deck)
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
            if event.data.get('type') == 'hit':
                card = event.data.get('message')
                print('card = ', card)
                self.players[1].add_cards(card[0], card[1])

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    sys.exit()
                self.event(event)
            self.screen.fill((0, 100, 0))
            self.render(self.screen)
            self.dealer.render(self.screen)
            for player in self.players:
                player.render(self.screen)
            pygame.display.flip()
