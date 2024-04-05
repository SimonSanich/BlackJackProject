import tkinter as tk
from tkinter import *

import pylab as p
from PIL import ImageTk
from PIL import Image
from Card import Card
from Deck import Deck
from Player import Player
from Dealer import Dealer


def BlackJackGame():
    root = tk.Tk()
    icon = Image.open('cards/blackjack.jpg')
    icon_photo = ImageTk.PhotoImage(icon)
    root.title(string="BlackJack")
    root.iconphoto(False, icon_photo)

    player = Player()
    dealer = Dealer()
    deck = Deck()
    deck.shuffle()

    global playerCardT, dealerCardT, imageCount
    playerCardT = 0
    dealerCardT = 0
    imageCount = 0

    def clear_frame():
        for widgets in frame_list[globals()['framecount']].winfo_children():
            widgets.destroy()
        frame_list[globals()['framecount']].destroy()

    def drawAdds(s, v):
        getCardString(s, v)

    def getCardString(s, v):
        if v == 1:
            valString = 'Ace'
        elif v == 11:
            valString = 'Jack'
        elif v == 12:
            valString = 'Queen'
        elif v == 13:
            valString = 'King'
        else:
            valString = str(v)
        fileName = "cards/" +s.lower() + "_" + valString+".png"
        addImage(fileName)

    def addImage(fileName):
        card = Image.open(fileName)
        cim = card.resize((95,145))
        im_card = ImageTk.PhotoImage(cim)
        image_list.append(im_card)

    global bet
    bet = 0
    def start_game():
        player.addChips(float(buyInEntry.get()))
        globals()['bet'] = float(betEntry.get())
        deal()

    global framecount
    framecount = 0
    def deal():
        clear_frame()
        globals()['framecount'] += 1
        frame_list[globals()['framecount']].pack(padx=1, pady=1)
        player.loseChips(globals()['bet'])

        player.draw(deck)
        drawAdds(player.getSuit(), player.getVal())
        label = Label(frame_list[globals()['framecount']], image=image_list[imageCount])
        label.place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100

        dealer.draw(deck)
        drawAdds(dealer.getSuit(), dealer.getVal())
        label = Label(frame_list[globals()['framecount']], image=image_list[imageCount])
        label.place(x=300 + globals()['dealerCardT'], y=100)
        globals()['imageCount'] += 1
        globals()['dealerCardT'] += 100

        player.draw(deck)
        drawAdds(player.getSuit(), player.getVal())
        label = Label(frame_list[globals()['framecount']], image=image_list[imageCount])
        label.place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100

        dealer.draw(deck)
        drawAdds(dealer.getSuit(), dealer.getVal())
        label = Label(frame_list[globals()['framecount']], image=image_list[imageCount])
        label.place(x=300 + globals()['dealerCardT'], y=100)
        globals()['imageCount'] += 1
        globals()['dealerCardT'] += 100

    frame_list = []
    image_list = []

    for i in range(0, 2000):
        frame_list.append(LabelFrame(root,
                                     width=955,
                                     height=800,
                                     background='green'))
    frame_list[0].pack()
    welcomeLabel = Label(
                    frame_list[0],
                    font=('JQKAs Wild', 15),
                    text="Hello, welcome to the Blackjack game"'\n'
                         "In this game, you have to win against the dealer by having 21 or close to it in your hand"'\n'
                         "Rules are simple. You can Hit to get a new card or you can Stand to reveal your hand and "
                         "thus ending the round.\n In the entries below, you must type the amount of chips you have "
                         "at the start of the game and your bet. \n The game is over when you run out of chips",
                    background='green')

    welcomeLabel.place(x=0, y=0)
    start_button = Button(frame_list[0],
                          text="Play BlackJack",
                          command=start_game,
                          height=1,
                          width=15,
                          background="grey",
                          font=('JQKAs Wild', 25, "bold")
                          )
    start_button.place(x=320, y=500)
    buyInEntry = Entry(frame_list[0], font=('JQKAs Wild', 25, "bold"))
    buyInEntry.place(x=400, y=650)
    buyInLabel = (Label(frame_list[0],
                        font=('JQKAs Wild', 25, "bold"),
                        text="Your Chips: ",
                        background='grey',
                        bd=2,
                        relief='solid',
                        highlightbackground='darkgrey'))
    buyInLabel.place(x=200, y=650)
    betEntry = Entry(frame_list[0], font=('JQKAs Wild', 25, "bold"))
    betEntry.place(x=400, y=750)
    betLabel = (Label(frame_list[0],
                      font=('JQKAs Wild', 25, "bold"),
                      text="Initial Bet: ",
                      background='grey',
                      bd=2,
                      relief='solid',
                      highlightbackground='darkgrey'))
    betLabel.place(x=200, y=750)

    root.mainloop()


BlackJackGame()
