class Dealer:

    def __init__(self):
        self.hand = []

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

