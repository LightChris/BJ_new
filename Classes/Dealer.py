from Classes.Card import *
import pygame


class Dealer:
    def __init__(self, pos):
        self.image = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.points = '0'
        self.pos = pos
        self.dx = 20  # Сдвиг карты
        self.cards = []  # [Card(), Card(), ...]

    @property
    def hand_points(self):
        return None

    def add_cards(self, rank, suit):
        # Добавляет карту диллеру
        card = Card(rank=rank, suit=suit)
        self.cards.append(card)

    def restart(self):
        self.image = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.cards = []

    def render(self, screen):
        dx = 0
        for card in self.cards:
            dx += self.dx
            card.render(self.image, (dx, 0))
        screen.blit(self.image, self.pos)

    @property
    def num_cards(self):
        return len(self.cards)
