class Player:

    def __init__(self):
        self.hand = []
        self.chips = 0

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

    def addChips(self, v):
        self.chips += v

    def loseChips(self, v):
        self.chips += v

    def getSuit(self):
        c = self.hand[len(self.hand)-1]
        return c.suit

    def getVal(self):
        c = self.hand[len(self.hand) - 1]
        return c.val
