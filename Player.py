class Player:

    def __init__(self):
        self.hand = []
        self.chips = 0
        self.splitToHolding = []

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

    def addChips(self, v):
        self.chips += v

    def loseChips(self, v):
        self.chips -= v

    def getSuit(self):
        c = self.hand[len(self.hand)-1]
        return c.suit

    def getVal(self):
        c = self.hand[len(self.hand) - 1]
        return c.val

    def chipCount(self):
        return self.chips
    # Basically what does ace do in every game if your hand consists of ace and for example 5 it creates a soft 16
    # hand which equals to 16 and 6 at the same time, but you cannot go bust with this type of hand because
    # if you for example then get a 10 which means that you should have overdrawn, and you should have 26
    # score instead get 16 because ace adjusts its value to 1 so that you won't go bust
    # This function for example checks whether the Ace is in your hand and if it is in your hand
    # then it checks the next card that you own and adjusts its value accordingly and counts the score
    # aceCard is a list which consists of the Aces, for correct score measurement they are added as the last element of
    # hand
    # Same explanation to DEALER.py

    def reset(self):
        self.hand = []

    def score(self):
        aceHand = False
        sum = 0
        count = 0
        for c in self.hand:
            if c.val == 1:
                aceCard = self.hand.pop(count)
                aceHand = True
            count += 1
        if not aceHand:
            for c in self.hand:
                if c.val == 1:
                    sum += 11
                elif c.val >= 10:
                    sum += 10
                else:
                    sum += c.val
        else:
            self.hand.append(aceCard)
            for c in self.hand:
                if c.val == 1:
                    if sum < 11:
                        sum += 11
                    else:
                        sum += 1
                elif c.val >= 10:
                    sum += 10
                else:
                    sum += c.val
        return sum

    def splitToHolding(self):
        self.splitToHolding.append(self.hand.pop())

    def splitCheck(self):
        if self.hand[0].val == self.hand[1].val:
            return True
        else:
            return False
