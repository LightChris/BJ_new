from Classes.Card import Card
import pygame


class Player:
    def __init__(self, pos, id, name='Player'):
        self.image = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.id = id
        self.points = '0'  # Сумма очков всех карт имеющихся у игрока
        self.name = name  # Имя игрока
        self.pos = pos  # Позиция игрока
        self.dx = 20  # Сдвиг карты
        self.cards = []  # Список карт

    def add_cards(self, rank, suit):
        """
        Добавляет карту в Список карт
        """
        card = Card(rank=rank, suit=suit)
        self.cards.append(card)

    def restart(self):
        """
        "Обнуляет" игрока
        """
        self.image = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.cards = []

    def render(self, screen):
        """
        Отображение поля и карт игрока на нем
        """
        dx = 0
        for card in self.cards:
            dx += self.dx
            card.render(self.image, (dx, 0))
        screen.blit(self.image, self.pos)
