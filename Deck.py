import random
from Card import Card


class Deck():
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
        # for i in range(1, 15):
        #   for j in range(len(self.cards) -1, 0, -1):
        #     r = random.randint(0, i)
        #    self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self):
        return self.cards.pop()

    def DeckReset(self):
        self.cards = []
        self.build()
