import random
from utilities import load_image
# from settings import PATH


class Card:
    """ Карты """

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.card_name = str(suit + rank) + '.png'
        # FIXME: загружать карты в соответствии с парметрами
        self.image = load_image(path="images/cards", name=self.card_name)

    def card_value(self):
        """ Возращает количество очков которое дает карта """
        if self.rank in "TJQK":
            # По 10 за десятку, валета, даму и короля
            return 10
        else:
            # Возвращает нужное число очков за любую другую карту
            # Туз изначально дает одно очко.
            return " A23456789".index(self.rank)

    def get_rank(self):
        return self.rank

    def render(self, screen, pos):
        screen.blit(self.image, pos)

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)


class Deck(object):
    """ Колода """

    def __init__(self):
        # ранги
        ranks = "23456789tjqka"
        # масти
        suits = "dchs"
        # генератор списков создающий колоду из 52 карт
        self.cards = [(s, r) for r in ranks for s in suits]
        # перетасовываем колоду. Не забудьте импортировать функцию shuffle из модуля random
        random.shuffle(self.cards)

    def deal_card(self):
        """ Функция сдачи карты """
        card = self.cards.pop(-1)
        return card[1], card[0]
