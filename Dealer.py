class Dealer:

    def __init__(self):
        self.hand = []

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)
    def getSuit(self):
        c = self.hand[len(self.hand)-1]
        return c.suit

    def getVal(self):
        c = self.hand[len(self.hand) - 1]
        return c.val

