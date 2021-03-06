import os
import sys
import pygame
from pgu import gui
from pygame import *
from settings import *
from ws_events import *
from Classes.Player import *
from Classes.Dealer import *
from utilities import load_image
from Classes.Server import Server
from Classes.LoginForm import LoginForm
from Classes.ConnectForm import ConnectForm
from Classes.ButtonsForm import ButtonsForm


class Game:
    def __init__(self, server):
        pygame.init()
        self.screen = pygame.display.set_mode((RESX, RESY), 0, 32)
        pygame.display.set_caption("BlackJack beta")
        self.myFont = pygame.font.SysFont("None", 16, bold=False, italic=False)
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

        # Игроки, Диллер
        self.players_position = [(275, 400), (25, 400), (525, 400)]
        self.dealer_position = (250, 75)
        self.current_player = None
        self.dealer = Dealer(self.dealer_position)
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
        self.dealer.render(screen)
        if self.current_player:
            self.current_player.render(screen)
            # current_player_font = self.myFont.render(str(self.current_player.name) + '  ' +
            #                                          str(self.current_player.points) + '/21', 0, (0, 0, 0))
            # screen.blit(current_player_font, (290, 380))
        for player in self.other_players:
            player.render(screen)
            # player_font = self.myFont.render(str(player.name) + '  ' + str(player.points) + '/21', 0, (0, 0, 0))
            # screen.blit(player_font, (player.pos[0] + 15, player.pos[1] - 20))
        screen.blit(self.deck_image, self.deck_pos)

    def event(self, event):
        self.buttons_form.event(event)
        self.connect_form.event(event)
        self.login_form.event(event)
        if event.type == WS_YOU_ID:
            self.current_id = event.id
            self.current_player = Player(self.players_position.pop(0), self.current_id)
            # self.current_player.name = event.name
        if event.type == WS_MESSAGE:
            if event.data.get('type') == 'hit' and event.data.get('id') == self.current_id:
                card = event.data.get('card')
                print('Вы получили карту:', card)
                self.current_player.add_cards(card[0], card[1])
            if event.data.get('type') == 'other_players':
                player = self.add_player(self.players_position.pop(0), event.data.get('id'))
                for card in event.data.get('hand'):
                    player.add_cards(card[1], card[0])
            if event.data.get('type') == 'new_client':
                self.add_player(self.players_position.pop(0), event.data.get('message'))
            if event.data.get('type') == 'hit' and event.data.get('id') == 'Dealer':
                card = event.data.get('card')
                self.dealer.add_cards(card[0], card[1])
            if event.data.get('id') != self.current_id:
                for player in self.other_players:
                    if player.id == event.data.get('id'):
                        player.points = str(event.data.get('points'))
            if self.current_player:
                if event.data.get('id') == self.current_id:
                    self.current_player.points = str(event.data.get('points'))
                    print("У вас " + self.current_player.points + " очков")
            if event.data.get('type') == 'bust':
                self.buttons_form.visible = False
                print("У вас перебор, ход закончен.")
            if event.data.get('type') == 'winner' and event.data.get('id') == self.current_id:
                print('Вы выиграли.')
            if event.data.get('type') == 'winner' and event.data.get('id') != self.current_id:
                print('Вы проиграли.')
            if event.data.get('type') == 'restart':
                self.current_player.restart()
                self.dealer.restart()
                for player in self.other_players:
                    player.restart()
                self.buttons_form.visible = True
            # if self.current_player:
            #     if event.data.get('id') == self.current_id:
            #         name = event.data.get('username')
            #         self.current_player.name = name
            if event.data.get('id') != self.current_id:
                for player in self.other_players:
                    if player.id == event.data.get('id'):
                        name = event.data.get('username')
                        player.name = name
            for player in self.other_players:
                if event.data.get('type') == 'hit' and player.id == event.data.get('id'):
                    card = event.data.get('card')
                    player.add_cards(card[0], card[1])

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    sys.exit()
                self.event(event)
            self.screen.fill((0, 100, 0))
            self.render(self.screen)
            pygame.display.flip()
