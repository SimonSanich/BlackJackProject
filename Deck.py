import random
from Card import Card
class Deck():
    def __init__(self):
        self.cards = []
        self.build()
    def build(self):
        for i in range (0,6):
            for s in ["Diamonds", "Hearts", "Clubs", "Spades"]:
                for v in range(1, 14):
                    self.cards.append(Card(v, s))
    def shuffle(self):
        for i in range(1,15):
            for j in range(len(self.cards) -1, 0, -1):
                r=random.randint(0,i)
                self.cards[i], self.cards[r]= self.cards[r],self.cards[i]
    def draw(self):
        return self.cards.pop()

    def DeckReset(self):
        self.cards = []
        self.build()
#У цьому класі використовується 6 колод та використовується різне значення для картинок. Щоб полегшити роботу можна
# замість використання 14 використати 10 та зменьшити сумарну кількість значеннь. А кожна 10 то буде вибіркою з списку
# "король", "дама", "валет" і власне сама 10. Реалізувати це можна використовуючи рандом.