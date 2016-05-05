from Classes.Card import Card
import pygame


class Player:
    def __init__(self, pos, deck):
        self.deck = deck
        self.image = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.pos = pos
        self.dx = 20  # Сдвиг карты
        self.cards = []  # [Card(), Card(), ...]

    @property
    def hand_points(self):
        return None

    def add_cards(self):
        # Добавляет карту игроку
        card = Card(*self.deck.deal_card())
        self.cards.append(card)

    def render(self, screen):
        dx = 0
        for card in self.cards:
            dx += self.dx
            card.render(self.image, (dx, 0))
        screen.blit(self.image, self.pos)

    @property
    def num_cards(self):
        return len(self.cards)
