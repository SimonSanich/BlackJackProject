class Player:

    def __init__(self):
        self.hand = []
        self.chips = 0
    def addChips(self):
        return
    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

    