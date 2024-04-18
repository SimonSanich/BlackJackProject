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
    root.attributes('-fullscreen', True)

    player = Player()
    dealer = Dealer()
    deck = Deck()
    deck.shuffle()

    global playerCardT, dealerCardT, imageCount, BJbool, downCardIndex
    playerCardT = 0
    dealerCardT = 0
    imageCount = 0
    BJbool = False
    downCardIndex = 0
    # function that clears frames

    def newGameFunc():
        hit_list[globals()['framecount']].destroy()
        stand_list[globals()['framecount']].destroy()
        again_list[globals()['framecount']].place(x=500, y=700)
        colorUp_list[globals()['framecount']].place(x=500, y=750)
    def clear_frame():
        for widgets in frame_list[globals()['framecount']].winfo_children():
            widgets.destroy()
        frame_list[globals()['framecount']].destroy()

    def drawAdds(s, v):
        getCardString(s, v)

    # function that creates cards from the deck

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
        fileName = "cards/" + s.lower() + "_" + valString + ".png"
        addImage(fileName)

    # function that creates an image of the card from getCardString

    def addImage(fileName):
        card = Image.open(fileName)
        cim = card.resize((95, 145))
        im_card = ImageTk.PhotoImage(cim)
        image_list.append(im_card)

    global bet
    bet = 0

    # function that takes the value from buyInEntry and gives it to bet which is players total bet size and starts deal

    def start_game():
        player.addChips(float(buyInEntry.get()))
        globals()['bet'] = float(betEntry.get())
        deal()

    global framecount
    framecount = 0

    def hit():
        player.draw(deck)
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300+globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100
        score_P = Label(frame_list[globals()['framecount']], text=str(player.score()), width=7, font=('JQKAs Wild', 25))
        score_P.place(x=350, y=680)
        if player.score() > 21:
            newGameFunc()
            Label(frame_list[globals()['framecount']], image=image_list[globals()['downCardIndex']]).place(x=300, y=100)
            Label(frame_list[globals()['framecount']],
                  text='Busted!',
                  width=12,
                  font=('JQKAs Wild', 25)).place(x=350, y=400)
            Label(frame_list[globals()['framecount']],
                  text='-'+str(globals()['bet']),
                  width=6,
                  fg='red',
                  font=('JQKAs Wild', 25)).place(x=350, y=350)

    def dealers_turn():
        Label(frame_list[globals()['framecount']], image=image_list[globals()['downCardIndex']]).place(x=300, y=100)
        while dealer.score() < 17:
            dealer.draw(deck)
            getCardString(dealer.getSuit(), dealer.getVal())
            Label(frame_list[globals()['framecount']],
                  image=image_list[imageCount]).place(x=300 + globals()['dealerCardT'], y=500)
            globals()['imageCount'] += 1
            globals()['playerCardT'] += 100

    def endgame():
        return

    def playerBJcheck():
        globals()["BJbool"] = True
        if player.score() == 21:
            newGameFunc()
            if dealer.score() == 21:
                player.addChips(globals()['bet'])
                Label(frame_list[globals()['framecount']],
                      text='Both Player and Dealer have BlackJack. Bet pushed.',
                      width=12,
                      font=('JQKAs Wild', 25)).place(x=350, y=400)
                Label(frame_list[globals()['framecount']],
                      text='+0' + str(globals()['bet'] * 1.5),
                      width=6,
                      fg='green',
                      font=('JQKAs Wild', 15)).place(x=100, y=800)
            else:
                Label(frame_list[globals()['framecount']],
                      text='BlackJack!!',
                      width=12,
                      font=('JQKAs Wild', 25)).place(x=350, y=400)
                player.addChips(globals()['bet']*2.5)
                Label(frame_list[globals()['framecount']],
                      text='+'+str(globals()['bet']*1.5),
                      width=6,
                      fg='green',
                      font=('JQKAs Wild', 15)).place(x=100, y=800)

    def dealerBJcheck():
        if dealer.score() == 21:
            Label(frame_list[globals()['framecount']], image=image_list[globals()['downCardIndex']]).place(x=300, y=100)
            newGameFunc()
            Label(frame_list[globals()['framecount']],
                  text='Dealer has a BlackJack!',
                  width=12,
                  font=('JQKAs Wild', 25)).place(x=350, y=400)
            Label(frame_list[globals()['framecount']],
                  text='-' + str(globals()['bet'] * 1.5),
                  width=6,
                  fg='green',
                  font=('JQKAs Wild', 15)).place(x=100, y=800)


    def deal():
        clear_frame()
        globals()['framecount'] += 1
        frame_list[globals()['framecount']].pack(padx=1, pady=1)
        player.loseChips(globals()['bet'])
        # adds a generated card to the player`s 'hand'
        player.draw(deck)
        drawAdds(player.getSuit(), player.getVal())
        label = Label(frame_list[globals()['framecount']], image=image_list[imageCount])
        label.place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100
        # adds a generated card to the dealer`s 'hand'
        dealer.draw(deck)
        drawAdds(dealer.getSuit(), dealer.getVal())
        globals()['downCardIndex'] = globals()['imageCount']
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

        score_P = Label(frame_list[globals()['framecount']], text=str(player.score()), width=7, font=('JQKAs Wild', 25))
        score_P.place(x=350, y=680)
    # temporarily disabled dealers score might return later
    # score_D = Label(frame_list[globals()['framecount']], text=str(dealer.score()), width=7, font=('JQKAs Wild', 25))
    # score_D.place(x=330, y=50)
        hit_list[globals()['framecount']].place(x=350, y=400)
        stand_list[globals()['framecount']].place(x=420, y=400)
        Label(frame_list[globals()['framecount']],
              width=15,
              text='Total Chips: ' + str(player.chipCount()),
              font=('JQKAs Wild', 25)). place(x=30, y=450)
        Label(frame_list[globals()['framecount']], image=chip_image).place(x=30, y=400)
        Label(frame_list[globals()['framecount']],
              width=7,
              text=str(globals()['bet']),
              font=('JQKAs Wild', 25)).place(x=80, y=400)
        playerBJcheck()

    frame_list = []
    image_list = []
    stand_list = []
    hit_list = []
    again_list = []
    colorUp_list = []
    # creates 2000 frames for every game cycle
    # creates buttons for stand and hit located on every frame starting from 1
    for i in range(0, 2000):
        frame_list.append(LabelFrame(root,
                                     width=1920,
                                     height=1080,
                                     background='green'))
        stand_list.append(Button(frame_list[i],
                                 text='stand',
                                 command=dealers_turn,
                                 height=2,
                                 width=5,
                                 background='grey',
                                 font=('JQKAs Wild', 15)))
        hit_list.append(Button(frame_list[i],
                               text='hit',
                               command=hit,
                               height=2,
                               width=5,
                               background='grey',
                               font=('JQKAs Wild', 15)))
        again_list.append(Button(frame_list[i],
                                 text='play again',
                                 command=deal,
                                 height=2,
                                 width=10,
                                 background='grey',
                                 font=('JQKAs Wild', 15)))
        colorUp_list.append(Button(frame_list[i],
                                   text='play again',
                                   command=dealers_turn,
                                   height=2,
                                   width=10,
                                   background='grey',
                                   font=('JQKAs Wild', 15)))
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

    ci = Image.open('cards/chip.png')
    chip_imag = ci.resize((40, 40))
    chip_image = ImageTk.PhotoImage(chip_imag)
    root.mainloop()


BlackJackGame()
