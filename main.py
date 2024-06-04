import tkinter as tk
from tkinter import *

from PIL import Image
from PIL import ImageTk
from Dealer import Dealer
from Deck import Deck
from Player import Player


def BlackJackGame():
    root = tk.Tk()
    icon = Image.open('cards/blackjack.jpg')
    icon_photo = ImageTk.PhotoImage(icon)
    root.title(string="BlackJack")
    root.iconphoto(False, icon_photo)
    root.attributes('-fullscreen', True)
    root.configure(background='grey')

    player = Player()
    dealer = Dealer()
    deck = Deck()
    deck.shuffle()

    global playerCardT, dealerCardT, imageCount, BJbool, downCardIndex, totalChips, doubleB, splitB
    totalChips = 0
    playerCardT = 0
    dealerCardT = 0
    imageCount = 0
    BJbool = False
    downCardIndex = 0
    doubleB = False
    splitB = False

    # function that clears frames

    def newGameFunc():
        hit_list[globals()['framecount']].destroy()
        stand_list[globals()['framecount']].destroy()
        again_list[globals()['framecount']].place(x=300, y=400)
        colorUp_list[globals()['framecount']].place(x=420, y=400)

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
        globals()['totalChips'] = float(buyInEntry.get())
        globals()['bet'] = float(betEntry.get())
        deal()

    global framecount
    framecount = 0

    def hit():
        doubleButton_list[globals()['framecount']].destroy()
        player.draw(deck)
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100
        score_P = Label(frame_list[globals()['framecount']], text=str(player.score()), width=7, font=('JQKAs Wild', 25))
        score_P.place(x=330, y=680)
        if player.score() > 21:
            if len(player.splitToHolding) > 0:
                hit_list[globals()['framecount']].destroy()
                stand_list[globals()['framecount']].destroy()
                nextSplitButton_List[globals()['framecount']].place(x=300, y=400)
                splitScore.append(player.score())
            elif globals()['splitB']:
                hit_list[globals()['framecount']].destroy()
                stand_list[globals()['framecount']].destroy()
                splitScore.append(player.score())
                dealerTurnButton_list[globals()['framecount']].place(x=300, y=400)
            else:
                newGameFunc()
                Label(frame_list[globals()['framecount']], image=image_list[globals()['downCardIndex']]).place(x=300,
                                                                                                               y=100)
                Label(frame_list[globals()['framecount']],
                      text='Busted!',
                      width=12,
                      font=('JQKAs Wild', 25)).place(x=330, y=680)
                Label(frame_list[globals()['framecount']],
                      text='-' + str(globals()['bet']),
                      width=6,
                      fg='red',
                      font=('JQKAs Wild', 25)).place(x=150, y=550)

    def dealers_turn():
        if len(player.splitToHolding) > 0:
            splitScore.append(player.score())
            splitDeal()
        else:
            doubleButton_list[globals()['framecount']].destroy()
            Label(frame_list[globals()['framecount']], image=image_list[globals()['downCardIndex']]).place(x=300, y=100)

            while dealer.score() < 17:
                dealer.draw(deck)
                getCardString(dealer.getSuit(), dealer.getVal())
                Label(frame_list[globals()['framecount']],
                      image=image_list[globals()['imageCount']]).place(x=300 + globals()['dealerCardT'], y=100)
                globals()['dealerCardT'] += 100
                globals()['imageCount'] += 1

            score_D = Label(frame_list[globals()['framecount']],
                            text=str(dealer.score()), width=7, font=('JQKAs Wild', 25))
            score_D.place(x=330, y=50)

            if dealer.score() > 21:
                if globals()["splitB"]:
                    splitScore.append(player.score())
                    splitResults()
                else:
                    newGameFunc()
                    splitButton_list[globals()['framecount']].destroy()
                    player.addChips(globals()['bet'] * 2)
                    Label(frame_list[globals()['framecount']],
                          text='Dealer Busted!',
                          width=12,
                          font=('JQKAs Wild', 25)).place(x=330, y=680)
                    Label(frame_list[globals()['framecount']],
                          text='+' + str(globals()['bet']),
                          width=6,
                          fg='green',
                          font=('JQKAs Wild', 25)).place(x=150, y=550)
            else:
                if globals()['splitB']:
                    splitScore.append(player.score())
                    splitResults()
                else:
                    checkWin()

    def doubleDown():
        doubleButton_list[globals()['framecount']].destroy()
        splitButton_list[globals()['framecount']].destroy()
        globals()['doubleB'] = True
        player.loseChips(globals()['bet'])
        globals()['bet'] *= 2

        Label(frame_list[globals()['framecount']],
              width=15,
              text='Total Chips ' + str(player.chipCount()),
              font=('JQKAs Wild', 25)).place(x=280, y=750)
        player.draw(deck)
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100
        Label(frame_list[globals()['framecount']],
              text=str(player.score()),
              width=7,
              font=('JQKAs Wild', 25)).place(x=350, y=680)
        if player.score() > 21:
            if len(player.splitToHolding) > 0:
                splitDouble.append(player.score())
                globals()['bet'] /= 2
                globals()['doubleB'] = False
                nextSplitButton_List[globals()['framecount']].place(x=300, y=400)
            elif globals()['splitB']:
                splitDouble.append(player.score())
                globals()['bet'] /= 2
                globals()['doubleB'] = False
                dealerTurnButton_list[globals()['framecount']].place(x=300, y=400)
            else:
                newGameFunc()
                Label(frame_list[globals()['framecount']],
                      image=image_list[globals()['downCardIndex']]).place(x=300, y=100)
                Label(frame_list[globals()['framecount']],
                      text='Busted!',
                      width=12,
                      font=('JQKAs Wild', 25)).place(x=350, y=680)
                Label(frame_list[globals()['framecount']],
                      text='-' + str(globals()['bet']),
                      width=6,
                      fg='red',
                      font=('JQKAs Wild', 25)).place(x=150, y=550)
        else:
            if len(player.splitToHolding) > 0:
                globals()['bet'] /= 2
                globals()['doubleB'] = False
                splitDouble.append(player.score())
                nextSplitButton_List[globals()['framecount']].place(x=300, y=400)
            elif globals()['splitB']:
                globals()['bet'] /= 2
                globals()['doubleB'] = False
                splitDouble.append(player.score())
                dealerTurnButton_list[globals()['framecount']].place(x=300, y=400)
            else:
                dealers_turn()

    def split():
        player.loseChips(globals()['bet'])
        globals()['playerCardT'] = 0
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        if not globals()['splitB']:
            dealer.splitHolding()
            dealer.splitHolding()

        globals()['splitB'] = True
        player.splitHolding()

        globals()['playerCardT'] = 100
        player.draw(deck)
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100
        Label(frame_list[globals()['framecount']],
              text=str(player.score()),
              width=7,
              font=('JQKAs Wild', 25)).place(x=330, y=680)
        Label(frame_list[globals()['framecount']],
              text='Split Hand 1',
              width=20,
              font=('JQKAs Wild', 25)).place(x=280, y=800)
        if not player.splitCheck():
            splitButton_list[globals()['framecount']].destroy()
        playerBJcheck()

    def splitDeal():
        clear_frame()
        globals()['framecount'] += 1
        frame_list[globals()['framecount']].pack(padx=1, pady=1)
        player.reset()
        globals()['playerCardT'] = 0
        globals()['dealerCardT'] = 0

        player.drawHolding()
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100

        dealer.drawHolding()
        getCardString(dealer.getSuit(), dealer.getVal())
        globals()['downCardIndex'] = globals()['imageCount']
        label = Label(frame_list[globals()['framecount']], image=dealerCard)
        label.place(x=300 + globals()['dealerCardT'], y=100)
        globals()['imageCount'] += 1
        globals()['dealerCardT'] += 100

        player.draw(deck)
        getCardString(player.getSuit(), player.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['playerCardT'], y=500)
        globals()['imageCount'] += 1
        globals()['playerCardT'] += 100

        dealer.drawHolding()
        getCardString(dealer.getSuit(), dealer.getVal())
        Label(frame_list[globals()['framecount']],
              image=image_list[imageCount]).place(x=300 + globals()['dealerCardT'], y=100)
        globals()['imageCount'] += 1
        globals()['dealerCardT'] += 100

        score_P = Label(frame_list[globals()['framecount']], text=str(player.score()), width=7, font=('JQKAs Wild', 25))
        score_P.place(x=350, y=680)

        hit_list[globals()['framecount']].place(x=300, y=400)
        stand_list[globals()['framecount']].place(x=375, y=400)
        doubleButton_list[globals()['framecount']].place(x=450, y=400)

        if player.splitCheck():
            splitButton_list[globals()['framecount']].place(x=560, y=400)

        Label(frame_list[globals()['framecount']],
              width=15,
              text='Total Chips: ' + str(player.chipCount()),
              font=('JQKAs Wild', 25)).place(x=280, y=750)
        #Label(frame_list[globals()['framecount']], image=chip_image).place(x=280, y=850)
        Label(frame_list[globals()['framecount']],
              width=20,
              text='Split Hand Continued',
              font=('JQKAs Wild', 25)).place(x=280, y=800)
        dealerBJcheck()
        playerBJcheck()


    def splitResults():
        newGameFunc()
        doubleButton_list[globals()['framecount']].destroy()
        splitButton_list[globals()['framecount']].destroy()
        dealerTurnButton_list[globals()['framecount']].destroy()
        Label(frame_list[globals()['framecount']],
              width=20,
              text='Split Hand Results ',
              font=('JQKAs Wild', 25)).place(x=280, y=800)
        Label(frame_list[globals()['framecount']],
              image=chip_image).place(x=50, y=400)
        Label(frame_list[globals()['framecount']],
              width=5,
              text=str(globals()['bet']),
              font=('JQKAs Wild', 25)).place(x=100, y=400)
        chipsCount = 0
        lossCount = 0
        winCount = 0
        tieCount = 0
        d_lossCount = 0
        d_winCount = 0
        d_tieCount = 0
        bjCount = 0
        for i in splitScore:
            if i > 21:
                chipsCount -= globals()['bet']
                lossCount += 1
            elif dealer.score() > 21:
                player.addChips(globals()['bet'] * 2)
                chipsCount += globals()['bet']
                winCount += 1
            elif i > dealer.score():
                player.addChips(globals()['bet'] * 2)
                chipsCount += globals()['bet']
                winCount += 1
            elif i == dealer.score():
                player.addChips(globals()['bet'])
                tieCount += 1
            else:
                chipsCount -= globals()['bet']
                lossCount += 1
        for i in splitDouble:
            if i > 21:
                chipsCount -= globals()['bet'] * 2
                d_lossCount += 1
            elif dealer.score() > 21:
                player.addChips(globals()['bet'] * 4)
                chipsCount += globals()['bet'] * 2
                d_winCount += 1
            elif i > dealer.score():
                player.addChips(globals()['bet'] * 4)
                chipsCount += globals()['bet'] * 2
                d_winCount += 1
            elif i == dealer.score():
                player.addChips(globals()['bet'] * 2)
                d_tieCount += 1
            else:
                chipsCount -= globals()['bet'] * 2
                d_lossCount += 1
        for i in splitBJ:
            player.addChips(globals()['bet'] * 2.5)
            chipsCount += globals()['bet'] * 2.5
            bjCount += 1
        if (d_winCount > 0 or d_lossCount > 0 or d_tieCount > 0) and bjCount > 0:
            Label(frame_list[globals()['framecount']],
                  text=' BlackJacks: ' + str(bjCount) +
                       ' Wins: ' + str(winCount) +
                       ' Loses: ' + str(lossCount) +
                       ' Tied: ' + str(tieCount) +
                       ' Double wins: ' + str(d_winCount) +
                       ' Double loses: ' + str(d_lossCount) +
                       ' Double ties: ' + str(d_tieCount),
                  width=80,
                  font=('JQKAs Wild', 25)).place(x=280, y=680)
        elif d_winCount > 0 or d_lossCount > 0 or d_tieCount > 0:
            Label(frame_list[globals()['framecount']],
                  text=" Win " + str(winCount) +
                       " Lost " + str(lossCount) +
                       " Tied " + str(tieCount) +
                       " Double Wins " + str(d_winCount) +
                       " Double Lost " + str(d_lossCount) +
                       " Double Tie " + str(d_tieCount),
                  width=80,
                  font=('JQKAs Wild', 25)).place(x=280, y=680)
        elif bjCount > 0:
            Label(frame_list[globals()['framecount']],
                  text=" BlackJacks " + str(bjCount) +
                       " Win " + str(winCount) +
                       " Lost " + str(lossCount) +
                       " Tied " + str(tieCount),
                  width=50,
                  font=('JQKAs Wild', 25)).place(x=280, y=680)
        else:
            Label(frame_list[globals()['framecount']],
                  text=" Win " + str(winCount) +
                       " Lost " + str(lossCount) +
                       " Tied " + str(tieCount),
                  width=20,
                  font=('JQKAs Wild', 25)).place(x=280, y=680)
        if chipsCount >= 0:
            Label(frame_list[globals()['framecount']], text='+' + str(chipsCount), width=6, fg='Green',
                  font=('JQKAs Wild', 25)).place(x=150, y=550)
        else:
            Label(frame_list[globals()['framecount']], text=str(chipsCount), width=6, fg='red',
                  font=('JQKAs Wild', 25)).place(x=150, y=550)

    def checkWin():
        newGameFunc()
        splitButton_list[globals()['framecount']].destroy()
        if player.score() > dealer.score():
            player.addChips(globals()['bet'] * 2)
            Label(frame_list[globals()['framecount']], text="Player Wins", width=12, font=('JQKAs Wild', 25)).place(
                x=330,
                y=680)
            Label(frame_list[globals()['framecount']], text="+" + str(globals()['bet']), width=6, fg='green',
                  font=('JQKAs Wild', 25)).place(x=150, y=550)
        elif player.score() == dealer.score():
            player.addChips(globals()['bet'])
            Label(frame_list[globals()['framecount']], text="Bets Pushed", width=12, font=('JQKAs Wild', 25)).place(
                x=330,
                y=680)
            Label(frame_list[globals()['framecount']], text="+0", width=6, font=('JQKAs Wild', 25)).place(x=150, y=550)
        else:
            Label(frame_list[globals()['framecount']], text="Dealer Wins", width=12, font=('JQKAs Wild', 25)).place(
                x=330,
                y=680)
            Label(frame_list[globals()['framecount']], text="-" + str(globals()['bet']), width=6, fg='red',
                  font=('JQKAs Wild', 25)).place(x=150, y=550)

    def endgame():
        finalChips = float(player.chipCount()) - globals()['totalChips']
        if finalChips >= 0:
            Label(root,
                  text='You won ' + str(finalChips) + ' Chips',
                  width=25,
                  font=('JQKAs Wild', 25),
                  background='grey',
                  fg='green').place(x=400, y=400)
        else:
            finalChips *= -1
            Label(root,
                  text='You lost ' + str(finalChips) + ' Chips',
                  width=25,
                  font=('JQKAs Wild', 25),
                  background='grey',
                  fg='red').place(x=400, y=400)
        clear_frame()

    def playerBJcheck():
        globals()["BJbool"] = True
        if player.score() == 21:
            doubleButton_list[globals()['framecount']].destroy()
            newGameFunc()
            if dealer.score() == 21:
                player.addChips(globals()['bet'])
                Label(frame_list[globals()['framecount']],
                      text='Both Player and Dealer have BlackJack. Bet pushed.',
                      width=50,
                      font=('JQKAs Wild', 25)).place(x=310, y=680)
                Label(frame_list[globals()['framecount']],
                      text='+0',
                      width=6,
                      fg='green',
                      font=('JQKAs Wild', 15)).place(x=150, y=550)
            else:
                Label(frame_list[globals()['framecount']],
                      text='BlackJack!!',
                      width=12,
                      font=('JQKAs Wild', 25)).place(x=330, y=680)
                if len(player.splitToHolding) > 0:
                    splitBJ.append(player.score())
                    colorUp_list[globals()['framecount']].destroy()
                    nextSplitButton_List[globals()['framecount']].place(x=300, y=400)
                elif globals()['splitB']:
                    splitBJ.append(player.score())
                    dealerTurnButton_list[globals()['framecount']].place(x=300, y=400)
                player.addChips(globals()['bet'] * 2.5)
                Label(frame_list[globals()['framecount']],
                      text='+' + str(globals()['bet'] * 1.5),
                      width=6,
                      fg='green',
                      font=('JQKAs Wild', 15)).place(x=150, y=550)

    def dealerBJcheck():
        if dealer.score() == 21:
            Label(frame_list[globals()['framecount']], image=image_list[globals()['downCardIndex']]).place(x=300, y=100)
            doubleButton_list[globals()['framecount']].destroy()
            splitButton_list[globals()['framecount']].destroy()
            newGameFunc()
            Label(frame_list[globals()['framecount']],
                  text='Dealer has a BlackJack!',
                  width=50,
                  font=('JQKAs Wild', 25)).place(x=310, y=680)
            Label(frame_list[globals()['framecount']],
                  text='-' + str(globals()['bet']),
                  width=8,
                  fg='red',
                  font=('JQKAs Wild', 25)).place(x=150, y=550)

    def deal():
        clear_frame()
        if globals()['doubleB']:
            globals()['bet'] /= 2
            globals()['doubleB'] = False
        splitScore.clear()
        splitDouble.clear()
        splitBJ.clear()
        player.splitHoldingReset()
        dealer.splitHoldingReset()
        player.reset()
        dealer.reset()
        globals()['splitB'] = False
        globals()['playerCardT'] = 0
        globals()['dealerCardT'] = 0

        globals()['framecount'] += 1
        frame_list[globals()['framecount']].pack(padx=1, pady=1)
        player.loseChips(globals()['bet'])

        deckLength = deck.length()
        if deckLength < 20:
            deck.DeckReset()
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
        label = Label(frame_list[globals()['framecount']], image=dealerCard)
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
        score_P.place(x=330, y=680)
        hit_list[globals()['framecount']].place(x=300, y=400)
        stand_list[globals()['framecount']].place(x=375, y=400)
        doubleButton_list[globals()['framecount']].place(x=450, y=400)

        if player.splitCheck():
            splitButton_list[globals()['framecount']].place(x=525, y=400)

        Label(frame_list[globals()['framecount']],
              width=15,
              text='Total Chips: ' + str(player.chipCount()),
              font=('JQKAs Wild', 25)).place(x=200, y=750)
        Label(frame_list[globals()['framecount']], image=chip_image).place(x=50, y=400)
        Label(frame_list[globals()['framecount']],
              width=7,
              text=str(globals()['bet']),
              font=('JQKAs Wild', 25)).place(x=100, y=400)
        dealerBJcheck()
        playerBJcheck()

    frame_list = []
    image_list = []
    stand_list = []
    hit_list = []
    again_list = []
    colorUp_list = []
    doubleButton_list = []
    splitButton_list = []
    dealerTurnButton_list = []
    nextSplitButton_List = []
    splitScore = []
    splitDouble = []
    splitBJ = []
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
                                   text='Finish playing',
                                   command=endgame,
                                   height=2,
                                   width=20,
                                   background='grey',
                                   font=('JQKAs Wild', 15)))
        doubleButton_list.append(Button(frame_list[i],
                                        text='double',
                                        command=doubleDown,
                                        height=2,
                                        width=5,
                                        background='grey',
                                        font=('JQKAs Wild', 15)))
        splitButton_list.append(Button(frame_list[i],
                                       text='split',
                                       command=split,
                                       height=2,
                                       width=5,
                                       background='grey',
                                       font=('JQKAs Wild', 15)))
        nextSplitButton_List.append(
            Button(frame_list[i], text="See Next Split",
                   command=splitDeal,
                   width=15,
                   height=2,
                   background='grey',
                   font=('JQKAs Wild', 25)))
        dealerTurnButton_list.append(
            Button(frame_list[i],
                   text="See Dealers Turn",
                   command=dealers_turn,
                   width=15,
                   height=2,
                   background='grey',
                   font=('JQKAs Wild', 25)))
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
    dj = Image.open('cards/deckColor.png')
    deckColor = dj.resize((95, 145))
    dealerCard = ImageTk.PhotoImage(deckColor)

    root.mainloop()


BlackJackGame()
