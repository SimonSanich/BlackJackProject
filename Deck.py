import random
from Card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for i in range(0, 6):
            for s in ["Diamonds", "Hearts", "Clubs", "Spades"]:
                for v in range(1, 14):
                    self.cards.append(Card(v, s))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def DeckReset(self):
        self.cards = []
        self.build()
