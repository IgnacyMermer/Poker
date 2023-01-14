import pygame
from pygame import *
from Events import *
from Card import *
from Components import *


class Player:
    """
    Class Player stores information about players, their position next to the table, 2 cards which they got,
    their account balance, how much money they spend in that round, round result, if they are still alive or maybe 
    they give up in that round and it stores information about risk level of that player, it doesn't matter if the player
    is user in front of the screen. 
    """


    def __init__(self, name, position, level = 1):
        self.name = name
        self.position = position
        self.cards = []
        self.roundResult = None
        self.currentMoney = 100
        self.moneyOnTable = 0
        self.currentAlive = "Alive"
        self.riskLevel = level

    def addCards(self, card):
        """This function add card to player's cards"""
        self.cards.append(card)
    
    def initCards(self):
        self.cards = []

    def choiceBestCards(self, communityCards):
        """This function void another functions which join user's cards and community's cards and choice the best 5 cards from seven and return result, 
        which is set to roundResult variable
        """

        tempList = self.cards + communityCards
        result = PokerHandler.getBestCards(tempList)
        self.roundResult = result

class Game:
    """
    This class is responsible for managing the entire game. It contains 7 states which tells program, in which moment of the game we are. 
    """

    STATE_START = 'start'
    STATE_PREPARING = 'preparing'
    STATE_PREFLOP = 'preflop'
    STATE_FLOP = 'flop'
    STATE_TURN = 'turn'
    STATE_RIVER = 'river'
    STATE_SHOWDOWN = 'showdown'


    def __init__(self, eventManager):
        """
        gameCards - it stores information about all cards in the cards pot
        eventManager is to add class' listener to it. It allows to call refresh funtion on every clock tick and check events and game states, 
        call another function on every moment of the game. In initial state it set game state on STATE_START, it call start function.
        """

        self.gameCards = GameCards()
        self.playersCount = 2
        self.myName = ""

        self.eventManager = eventManager
        self.eventManager.addListener(self)

        self.playerSprites = pygame.sprite.RenderUpdates()
        self.state = Game.STATE_START
        self.moneyText = ""
        self.isFirstTime = True


    def refresh(self, event):
        if isinstance(event, GameStartEvent):
            if event.playersCount != -1:
                self.playersCount = 1 + event.playersCount
                if self.state == Game.STATE_START:
                    self.start()
            else:
                self.state = Game.STATE_START
                self.isFirstTime = True
                self.startNextRound()

        elif isinstance(event, NextMoveEvent):
            if self.state == Game.STATE_PREPARING:
                self.dealPreflop()
            elif self.state == Game.STATE_PREFLOP:
                self.dealFlop()
            elif self.state == Game.STATE_FLOP:
                self.dealTurn()
            elif self.state == Game.STATE_TURN:
                self.dealRiver()
            elif self.state == Game.STATE_RIVER:
                self.showDown()
        if isinstance(event, MoneyTextEvent):
            if self.state == Game.STATE_START:
                self.myName = event.text
            else:
                self.moneyText = event.text

    def start(self):
        self.initializePlayers()
        self.initializeRound()
        self.eventManager.addEventToQueue(ClearMoneyEvent())
        self.eventManager.addEventToQueue(MoneyTextEvent(""))
    
    def startNextRound(self):
        self.initializeRound()
        self.eventManager.addEventToQueue(ClearMoneyEvent())
        self.eventManager.addEventToQueue(MoneyTextEvent(""))
        self.eventManager.addEventToQueue(NextMoveEvent())

    def initializeRound(self):
        self.state = Game.STATE_PREPARING
        self.communityCards = []
        self.money = 0
        self.highestMoney = 0
        self.gameCards.initializeCards()
        self.gameCards.mixCards()

    
    def initializePlayers(self):
        self.players = []
        self.players.append(Player(self.myName, 0, 0))
        nameList=['Zdzichu', 'Zbychu', 'Damcio', 'Pawcio']
        for i in range(1, self.playersCount):
            self.players.append(Player(nameList[i], i, 2))


    def dealPreflop(self):
        """
        In this moment of game, players get two first cards and then they start auction
        """

        self.state = Game.STATE_PREFLOP
        playerCount = len(self.players)

        for i in range(playerCount * 2):
            self.players[i%playerCount].addCards(self.gameCards.popCard())

        self.eventManager.addEventToQueue(PreFlopEvent(self.players))
    
    def dealFlop(self):

        """
        Here is call function (firstMoney) responds for handling first auction in round, then computer shows 3 community cards.
        """
        self.firstMoney()
        if not self.checkIfEnd():
            tempBool = True
            self.eventManager.addEventToQueue(ClearMoneyEvent())
            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                self.state = Game.STATE_FLOP
                for i in range(3):
                    self.communityCards.append(self.gameCards.popCard())
                
                self.isFirstTime = True
                self.eventManager.addEventToQueue(FlopEvent(self.communityCards, self.players))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_RIVER
            playerAlive = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players, playerAlive, self.communityCards, playerAlive.cards))
    
    def firstMoney(self):
        """
        This is void handling first auction, it gets input from user or allows to resign for that round if user writes p in input, 
        It takes user's price and check for every computer player if it should resign or take the same bid or put more money. 
        It decide it based on player's cards and risk level of the player.
        """
        
        highestPrice = self.highestMoney
        price = 0
        if self.isFirstTime:
            player = self.players[0]
            kwota = self.moneyText
            self.moneyText = ""
            try:
                price = int(kwota)
                if price > player.currentMoney/2 or price < 1:
                    raise ValueError('Niepoprawna wartość kwoty licytacji')
                highestPrice = price
                player.currentMoney -= price
                player.moneyOnTable += price
            except:
                raise TypeError('Nie została prawidłowo podana kwota licytacji')
        else:
            player = self.players[0]
            if player.moneyOnTable < highestPrice:
                kwota = self.moneyText
                if kwota == 'p':
                    player.currentAlive = 'OOTR'
                elif kwota == 'w':
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                else:
                    try:
                        price = int(kwota)
                        if price > player.currentMoney/2 or price < 1:
                            raise ValueError('Niepoprawna wartość kwoty licytacji')
                        if price < highestPrice - player.moneyOnTable:
                            player.currentAlive = 'OOTR'
                            price = 0
                            print('Za mala kwota aby wyrownac lub podbic')
                        highestPrice = price + player.moneyOnTable
                        player.currentMoney -= price
                        player.moneyOnTable += price
                    except:
                        raise TypeError('Nie została prawidłowo podana kwota licytacji')
        self.isFirstTime = False
        for i in range(1, len(self.players)):
            player = self.players[i]
            if highestPrice - player.moneyOnTable >= player.currentMoney:
                player.currentAlive = 'OOTR'
            elif player.currentAlive == 'Alive' and highestPrice > player.moneyOnTable:
                if highestPrice > 0 and highestPrice < 20:
                    if PokerHandler.getTwoCardResult(self.players[1].cards).score > 18 and \
                    self.players[1].riskLevel > 1:
                            highestPrice = 35
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice >= 20 and highestPrice <= 40:
                    if PokerHandler.getTwoCardResult(player.cards).score > 18:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                else:
                    if PokerHandler.getTwoCardResult(player.cards).score > 100:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
        
        self.highestMoney = highestPrice
    
    def dealTurn(self):

        self.secondMoney()
        if not self.checkIfEnd():
            self.eventManager.addEventToQueue(ClearMoneyEvent())
            
            tempBool = True
            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                for player in self.players:
                    (player.name+' '+player.currentAlive)
                self.state = Game.STATE_TURN
                tempCards = self.gameCards.popCard()
                self.communityCards.append(tempCards)

                self.isFirstTime = True
                self.eventManager.addEventToQueue(TurnEvent(tempCards, self.players))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_RIVER
            playerAlive = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players, playerAlive, self.communityCards, playerAlive.cards))

    def secondMoney(self):
        highestPrice = self.highestMoney
        player1Cards = self.players[1].cards + self.communityCards
        player2Cards = []
        if len(self.players) > 2:
            player2Cards = self.players[2].cards + self.communityCards
        player3Cards = []
        if len(self.players) > 3:
            self.players[3].cards + self.communityCards
        playersCards = [player1Cards, player2Cards, player3Cards]
        if self.players[0].currentAlive == 'Alive':
            price = 0
            if self.isFirstTime:
                player = self.players[0]
                kwota = self.moneyText
                try:
                    price = int(kwota)
                    if price > player.currentMoney or price < 1:
                        raise ValueError('Niepoprawna wartość kwoty licytacji')
                    highestPrice += price
                    player.currentMoney -= price
                    player.moneyOnTable += price
                    
                except:
                    raise TypeError('Nie została prawidłowo podana kwota licytacji')
            else:
                player = self.players[0]
                if player.moneyOnTable < highestPrice:
                    kwota = self.moneyText
                    if kwota == 'p':
                        player.currentAlive = 'OOTR'
                    elif kwota == 'w':
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        try:
                            price = int(kwota)
                            if price > player.currentMoney or price < 1:
                                raise ValueError('Niepoprawna wartość kwoty licytacji')
                            if price < highestPrice - player.moneyOnTable:
                                player.currentAlive = 'OOTR'
                                price = 0
                                print('Za mala kwota aby wyrownac lub podbic')
                            highestPrice += price
                            player.currentMoney -= price
                            player.moneyOnTable += price
                        except:
                            raise TypeError('Nie została prawidłowo podana kwota licytacji')
        self.isFirstTime = False
        for i in range(1, len(self.players)):
            player = self.players[i]
            if player.currentAlive == 'Alive' and highestPrice > player.moneyOnTable:
                if highestPrice < 35 and highestPrice <= player.currentMoney:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 100:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and 45 <= player.currentMoney:
                                highestPrice = 40
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 38 <= player.currentMoney:
                                highestPrice = 35
                            elif 35 <= player.currentMoney:
                                highestPrice = 35
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and 50 <= player.currentMoney:
                                highestPrice = 50
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 45 <= player.currentMoney:
                                highestPrice = 45
                            elif 40 <= player.currentMoney:
                                highestPrice = 40
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice >= 35 and highestPrice <= 45:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 50 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 45 and highestPrice <= 50:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 250 and highestPrice <= player.currentMoney:
                        if player.riskLevel > 1 and 60 <= player.currentMoney:
                            highestPrice = 60
                        elif player.riskLevel > 0 and 57 <= player.currentMoney:
                            highestPrice = 52
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 100 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 50 and highestPrice <= 60:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 300 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 700 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1500 and highestPrice <= player.currentMoney:
                        if 60 <= player.currentMoney:
                            highestPrice = 60
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                else:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
        self.highestMoney = highestPrice

    def dealRiver(self):

        self.thirdMoney()
        if not self.checkIfEnd():

            self.eventManager.addEventToQueue(ClearMoneyEvent())
            
            tempBool = True
            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                for player in self.players:
                    (player.name+' '+player.currentAlive)
                self.state = Game.STATE_RIVER
                tempCards = self.gameCards.popCard()
                self.communityCards.append(tempCards)

                self.isFirstTime = True
                self.eventManager.addEventToQueue(RiverEvent(tempCards, self.players))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_RIVER
            playerAlive = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players, playerAlive, self.communityCards, playerAlive.cards))

    def thirdMoney(self):
        highestPrice = self.highestMoney
        player1Cards = self.players[1].cards + self.communityCards
        player2Cards = []
        if len(self.players) > 2:
            player2Cards = self.players[2].cards + self.communityCards
        player3Cards = []
        if len(self.players) > 3:
            self.players[3].cards + self.communityCards
        playersCards = [player1Cards, player2Cards, player3Cards]
        if self.players[0].currentAlive == 'Alive':
            price = 0
            if self.isFirstTime:
                player = self.players[0]
                kwota = self.moneyText
                try:
                    price = int(kwota)
                    if price > player.currentMoney or price < 1:
                        raise ValueError('Niepoprawna wartość kwoty licytacji')
                    highestPrice += price
                    player.currentMoney -= price
                    player.moneyOnTable += price
                    
                except:
                    raise TypeError('Nie została prawidłowo podana kwota licytacji')
            else:
                player = self.players[0]
                if player.moneyOnTable < highestPrice:
                    kwota = self.moneyText
                    if kwota == 'p':
                        player.currentAlive = 'OOTR'
                    elif kwota == 'w':
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        try:
                            price = int(kwota)
                            if price > player.currentMoney or price < 1:
                                raise ValueError('Niepoprawna wartość kwoty licytacji')
                            if price < highestPrice - player.moneyOnTable:
                                player.currentAlive = 'OOTR'
                                price = 0
                                print('Za mala kwota aby wyrownac lub podbic')
                            highestPrice += price
                            player.currentMoney -= price
                            player.moneyOnTable += price
                        except:
                            raise TypeError('Nie została prawidłowo podana kwota licytacji')
        self.isFirstTime = False
        
        for i in range(1, len(self.players)):
            player = self.players[i]
            if player.currentAlive == 'Alive' and highestPrice > player.moneyOnTable:
                if highestPrice < 40 and highestPrice <= player.currentMoney:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 200:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and 55 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 55
                            elif PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and 49 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 49
                            elif 44 <= player.currentMoney:
                                highestPrice = 44
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and 58 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 58
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 54 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 54
                            elif 50 <= player.currentMoney:
                                highestPrice = 50
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice >= 40 and highestPrice <= 50:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 200:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and 55 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 55
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and 58 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 64
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 54 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 58
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
                elif highestPrice > 50 and highestPrice <= 55:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and highestPrice <= player.currentMoney:
                        if player.riskLevel > 1 and 66 <= player.currentMoney:
                            highestPrice = 66
                        elif player.riskLevel > 0 and 60 <= player.currentMoney:
                            highestPrice = 60
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score > 130 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 55 and highestPrice <= 60:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 150 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 250 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1500 and highestPrice <= player.currentMoney:
                        if 70 <= player.currentMoney:
                            highestPrice = 70
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 60 and highestPrice <= 65:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 200 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 300 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1800 and highestPrice <= player.currentMoney:
                        if 70 <= player.currentMoney:
                            highestPrice = 70
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 2500 and highestPrice <= player.currentMoney:
                        if 75 <= player.currentMoney:
                            highestPrice = 75
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 65 and highestPrice <= 70:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 300 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and highestPrice <= player.currentMoney:
                        if 74 <= player.currentMoney:
                            highestPrice = 74
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3000 and highestPrice <= player.currentMoney:
                        if 79 <= player.currentMoney:
                            highestPrice = 79
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 70 and highestPrice <= 75:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 400 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1500 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3000 and player.riskLevel == 1 and highestPrice <= player.currentMoney:
                        if 76 <= player.currentMoney:
                            highestPrice = 76
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 84 <= player.currentMoney:
                            highestPrice = 84
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 75 and highestPrice <= 80:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 500 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 4000 and player.riskLevel == 1 and highestPrice <= player.currentMoney:
                        if 82 <= player.currentMoney:
                            highestPrice = 82
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 86 <= player.currentMoney:
                            highestPrice = 86
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 80 and highestPrice <= 85:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3500 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5500 and player.riskLevel == 1 and highestPrice <= player.currentMoney:
                        if 86 <= player.currentMoney:
                            highestPrice = 86
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 6500 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 88 <= player.currentMoney:
                            highestPrice = 88
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice > 85 and highestPrice <= 90:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 1500 and player.riskLevel > 1 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 4000 and player.riskLevel > 0 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 6000 and player.riskLevel == 1 and highestPrice <= player.currentMoney:
                        if 91 <= player.currentMoney:
                            highestPrice = 91
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 7500 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 94 <= player.currentMoney:
                            highestPrice = 94
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                else:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
        self.highestMoney = highestPrice
    
    def checkIfEnd(self):
        countAlive = 0
        for player in self.players:
            if player.currentAlive == 'Alive':
                countAlive += 1
        if countAlive > 1:
            return False
        return True
    
    def showDown(self):
        self.state = Game.STATE_SHOWDOWN
        for player in self.players:
            player.choiceBestCards(self.communityCards)
        if self.players[0].currentAlive != 'Alive' or self.players[0].moneyOnTable != 0:
            winner = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players, winner, self.communityCards, winner.cards))


    def getWinner(self):
        bestScore = 0
        bestPlayer = None
        allMoneyOnTable = 0
        for player in self.players:
            if player.roundResult is not None:
                if player.roundResult.score > bestScore and player.currentAlive == 'Alive':
                    bestScore = player.roundResult.score
                    bestPlayer = player
            else:
                if player.currentAlive == 'Alive' and bestScore == 0:
                    bestPlayer = player
            allMoneyOnTable += player.moneyOnTable
            player.moneyOnTable = 0
            #player.roundResult = None
            player.currentAlive = 'Alive'
            player.cards = []

        bestPlayer.currentMoney += allMoneyOnTable
        return bestPlayer


class TextSprite(pygame.sprite.Sprite):

    def __init__(self, text, position, size, color, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.fontcolor = color
        self.fontsize = size
        self.text = text

        textSurf = self.writeSomething(self.text)
        self.image = textSurf
        self.rect = textSurf.get_rect()
        self.position = position
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]
        self.canMove = False
        self.prev_x_pos = None
        self.canMakeBiggerFont = False
        self.repeat_cnt = 0
        self.prev_font_size = self.fontsize
        self.dest_font_size = 60


    def writeSomething(self, msg=""):
        myfont = pygame.font.SysFont("None", self.fontsize)
        mytext = myfont.render(msg, True, self.fontcolor)
        mytext = mytext.convert_alpha()
        return mytext

    def update(self, seconds):
        textSurf = self.writeSomething(self.text)
        self.image = textSurf
        self.rect = textSurf.get_rect()
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]


class CardSprite(pygame.sprite.Sprite):

    def __init__(self, card, pos1,  pos2, type, image = '', group=None):
        pygame.sprite.Sprite.__init__(self, group)
        if image == '':
            image = pygame.image.load(self.GetCardImageName(card))
        else:
            image = pygame.image.load(image)
        self.srcImage = image
        self.image = self.srcImage
        self.pos = [0.0, 0.0]
        self.pos[0] = pos1[0] * 1.0
        self.pos[1] = pos1[1] * 1.0
        self.pos2 = pos2
        self.pos1 = pos1
        self.type = type
        self.rect = self.srcImage.get_rect()

    def update(self, seconds):
        if(self.type == Card.PLAYER_CARD or self.type == Card.COMMUNITY_CARD):
            if self.pos2[0] - self.pos1[0] < 0 \
                and self.pos2[0] <= self.pos[0]:
                self.pos[0] += self.GetDelX(0.6, seconds)
                if self.pos[0] <= self.pos2[0]:
                    self.pos[0] = self.pos2[0]
            if self.pos2[0] - self.pos1[0] >= 0 \
                and self.pos2[0] >= self.pos[0]:
                self.pos[0] += self.GetDelX(0.6, seconds)
                if self.pos[0] >= self.pos2[0]:
                    self.pos[0] = self.pos2[0]
            if self.pos2[1] - self.pos1[1] < 0 \
                and self.pos2[1] <= self.pos[1]:
                self.pos[1] += self.GetDelY(0.6, seconds)
                if self.pos[1] <= self.pos2[1]:
                    self.pos[1] = self.pos2[1]
            if self.pos2[1] - self.pos1[1] >= 0 \
                and self.pos2[1] >= self.pos[1]:
                self.pos[1] += self.GetDelY(0.6, seconds)
                if self.pos[1] >= self.pos2[1]:
                    self.pos[1] = self.pos2[1]

        self.rect.centerx = round(self.pos[0], 0)
        self.rect.centery = round(self.pos[1], 0)

    def GetDelX(self, speed, seconds):
        return (-1.0) *(self.pos1[0] - self.pos2[0]) / seconds / speed

    def GetDelY(self, speed, seconds):
        return (-1.0) *(self.pos1[1] - self.pos2[1]) / seconds / speed

    def GetCardImageName(self, card):
            color = card.getColor()
            rank = card.getRank()

            colorStr = ''
            rankStr = ''

            if color == 0:
                colorStr = 'wino'
            elif color == 1:
                colorStr = 'dzwonek'
            elif color == 2:
                colorStr = 'serce'
            elif color == 3:
                colorStr = 'zoladz'

            if rank == 13:
                rankStr = 'as'
            elif rank > 0 and rank < 10:
                rankStr = str(rank +1)
            elif rank == 10:
                rankStr = 'jopek'
            elif rank == 11:
                rankStr = 'dama'
            elif rank == 12:
                rankStr = 'krol'

            tempStr = f'images/{rankStr}_{colorStr}.png'
            return tempStr

class EventListener:

    def __init__(self):
        self.listeners = {}
        self.events = []
        self.newListeners = []
        self.oldListeners = []

    def addListener(self, listener):
        self.newListeners.append(listener)

    def refreshListeners(self):
        for listener in self.newListeners:
            self.listeners[listener] = 1
        for listener in self.oldListeners:
            if listener in self.listeners:
                del self.listeners[listener]

    def removeListener(self, listener):
        self.oldListeners.append(listener)
    
    def voidEvents(self):
        for event in self.events:
            for listener in self.listeners:
                listener.refresh(event)
            if self.newListeners:
                self.refreshListeners()
        self.events = []
    
    def addEventToQueue(self, event):
        self.events.append(event)
        if isinstance(event, ClockEvent):
            self.refreshListeners()
            self.voidEvents()

class KeyboardController:

    def __init__(self, eventManager, playerName=None):
        self.eventManager = eventManager
        self.eventManager.addListener(self)
        self.moneyText = ""

    def refresh(self, event):
        if isinstance(event, ClockEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == pygame.QUIT:
                    ev = QuitEvent()
                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    ev = QuitEvent()

                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    ev = NextMoveEvent()

                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RIGHT:
                    ev = GameStartEvent(-1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.moneyText = self.moneyText[:-1]
                    else:
                        self.moneyText += event.unicode
                    ev = MoneyTextEvent(self.moneyText)
                if ev:
                    self.eventManager.addEventToQueue(ev)
        if isinstance(event, ClearMoneyEvent):
            self.moneyText = ""


class TableSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        tableSurf = pygame.Surface((1400, 800))
        tableSurf = tableSurf.convert_alpha()
        tableSurf.fill((0, 0, 0, 0))

        self.image = tableSurf
        self.rect = (0, 0)



class PygameView:

    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.addListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption('Poker')
        
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((35, 85, 35))

        self.window.blit(self.background, (0, 0))

        font = pygame.font.Font(None, 60)
        textSurf = font.render("Poker Texas Holdem", True, (150, 150, 150))
        textSurf = textSurf.convert_alpha()
        
        self.window.blit(textSurf, ((1400 - textSurf.get_width())/2, 150))

        image1 = pygame.image.load('images/btn1przeciwnik.png').convert_alpha()
        self.rect = image1.get_rect()

        self.button1 = Button('images/btn1przeciwnik.png', 1400, 200, self.window)
        self.button2 = Button('images/btn2przeciwnik.png', 1400, 300, self.window)
        self.button3 = Button('images/btn3przeciwnik.png', 1400, 400, self.window)


        textSurf2 = font.render("Podaj imie", True, (150, 150, 150))
        textSurf2 = textSurf2.convert_alpha()
        
        self.window.blit(textSurf2, (150, 200))
        

        font = pygame.font.SysFont(None, 100)
        self.text = ""
        self.inputActive = True
        self.inputRect = pygame.Rect(200, 200, 140, 32)

        self.gameStarted = False

        self.clock = pygame.time.Clock()
        self.run = True

        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.playerSprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()

        self.betsSprites = []
        self.betsMoneySprites = []
        self.moneyText = ''


    def refresh(self, event):
        if isinstance(event, ClockEvent):

            if self.run:
                eventList = pygame.event.get()
                for event in eventList:
                    if event.type == pygame.QUIT:
                        self.run = False


            if self.button1.onClick() and not self.gameStarted:
                self.eventManager.addEventToQueue(GameStartEvent(1))
                self.gameStarted = True
                self.eventManager.addEventToQueue(NextMoveEvent())
            if self.button2.onClick() and not self.gameStarted:
                self.eventManager.addEventToQueue(GameStartEvent(2))
                self.gameStarted = True
                self.eventManager.addEventToQueue(NextMoveEvent())
            if self.button3.onClick() and not self.gameStarted:
                self.eventManager.addEventToQueue(GameStartEvent(3))
                self.gameStarted = True
                self.eventManager.addEventToQueue(NextMoveEvent())

            self.backSprites.clear(self.window, self.background)
            self.playerSprites.clear(self.window, self.background)
            self.communitySprites.clear(self.window, self.background)

            self.backSprites.update(60)
            self.playerSprites.update(60)
            self.communitySprites.update(60)

            sprites1 = self.backSprites.draw(self.window)
            sprites2 = self.playerSprites.draw(self.window)
            sprites3 = self.communitySprites.draw(self.window)

            sprites= sprites1 + sprites2 + sprites3
            pygame.display.update(sprites)

        if isinstance(event, GameStartEvent):
            for sprite in self.backSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.playerSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.communitySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.betsSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.betsMoneySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            self.playerSprites = pygame.sprite.RenderUpdates()
            self.communitySprites = pygame.sprite.RenderUpdates()

            self.betsSprites = []
            self.betsMoneySprites = []
            TableSprite(self.backSprites)

        if isinstance(event, MoneyTextEvent):
            for sprite in self.betsMoneySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            self.moneyText = event.text
            self.betsMoneySprites.append(TextSprite(event.text + " $", (700, 90), 30, (150, 150, 150), self.playerSprites))
        
        if isinstance(event, MoneyToEquals):
            for sprite in self.betsMoneySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.betsSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            self.moneyText = ""
            self.betsSprites.append(TextSprite(event.text, (700, 50), 30, (150, 150, 150), self.playerSprites))

        if isinstance(event, PreFlopEvent):
            firstLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.players[0].currentMoney/2}$)', (700, 50), 30, (150, 150, 150), self.playerSprites)
            self.betsSprites.append(firstLicitacja)
            self.showPreFlopCards(event.players)

        if isinstance(event, FlopEvent):
            for sprite in self.betsMoneySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.betsSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            secondLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.playersList[0].currentMoney}$)', (700, 50), 30, (150, 150, 150), self.playerSprites)
            self.betsSprites.append(secondLicitacja)
            self.showCommunityCards(event.cardList, event.playersList)

        if isinstance(event, TurnEvent):
            for sprite in self.betsMoneySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.betsSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            thirdLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.playersList[0].currentMoney}$)', (700, 50), 30, (150, 150, 150), self.playerSprites)
            self.betsSprites.append(thirdLicitacja)
            self.showTurnCard(event.card, event.playersList)

        if isinstance(event, RiverEvent):
            for sprite in self.betsMoneySprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            for sprite in self.betsSprites:
                sprite.kill()
                sprite.rect = None
                sprite.image = None
            thirdLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.playersList[0].currentMoney}$)', (700, 50), 30, (150, 150, 150), self.playerSprites)
            self.showRiverCard(event.card, event.playersList)

        if isinstance(event, ShowDownEvent):
            self.showDownResult(event.players, event.player, event.communityCards, event.cardList)

    def showPreFlopCards(self, players):

        POS_LEFT = 0
        POS_TOP = 0

        for i in range(len(players)):
            player = players[i]
            playerPos = player.position

            if playerPos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif playerPos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif playerPos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif playerPos == 3:
                POS_LEFT = 1150
                POS_TOP = 210

            imageSrc = 'images/niewiadoma.png' if i != 0 else ''
            CardSprite(player.cards[0], Card.CARDS_POSITION, (POS_LEFT - 85, POS_TOP), Card.PLAYER_CARD, imageSrc, self.playerSprites)
            CardSprite(player.cards[1], Card.CARDS_POSITION, (POS_LEFT + 14, POS_TOP), Card.PLAYER_CARD, imageSrc, self.playerSprites)
            TextSprite(player.name, (POS_LEFT - 20, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites)


    def showCommunityCards(self, cardList, players):
        self.scoreSprites = []
        for player in players:
            playerPos = player.position
            POS_LEFT = 0
            POS_TOP = 0

            if playerPos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif playerPos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif playerPos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif playerPos == 3:
                POS_LEFT = 1150
                POS_TOP = 210
            if player.currentAlive == 'Alive':
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 30, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
            else:
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite('Poza runda', (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
        i = 0
        for card in cardList:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 350), Card.COMMUNITY_CARD, '', self.communitySprites)

    def showTurnCard(self, card, players):
        for sprite in self.scoreSprites:
            sprite.rect = None
            sprite.image = None
            sprite.kill()
        self.scoreSprites = []

        for player in players:
            playerPos = player.position
            POS_LEFT = 0
            POS_TOP = 0

            if playerPos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif playerPos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif playerPos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif playerPos == 3:
                POS_LEFT = 1150
                POS_TOP = 210

            if player.currentAlive == 'Alive':
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 30, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
            else:
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite('Poza runda', (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
        CardSprite(card, Card.CARDS_POSITION, (750, 350), Card.COMMUNITY_CARD, '', self.communitySprites)

    def showRiverCard(self, card, players):
        for sprite in self.scoreSprites:
            sprite.rect = None
            sprite.image = None
            sprite.kill()
        self.scoreSprites = []

        for player in players:
            playerPos = player.position
            POS_LEFT = 0
            POS_TOP = 0

            if playerPos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif playerPos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif playerPos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif playerPos == 3:
                POS_LEFT = 1150
                POS_TOP = 210

            if player.currentAlive == 'Alive':
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 30, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
            else:
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite('Poza runda', (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
        CardSprite(card, Card.CARDS_POSITION, (850, 350), Card.COMMUNITY_CARD, '', self.communitySprites)
    
    def showDownResult(self, players, player, communityCards, cardsList):
        for sprite in self.scoreSprites:
            sprite.rect = None
            sprite.image = None
            sprite.kill()
        self.scoreSprites = []

        for playerTemp in players:
            playerPos = playerTemp.position
            POS_LEFT = 0
            POS_TOP = 0

            if playerPos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif playerPos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif playerPos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif playerPos == 3:
                POS_LEFT = 1150
                POS_TOP = 210
            self.scoreSprites.append(TextSprite(str(playerTemp.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))

        for cardSprite in self.communitySprites:
            cardSprite.kill()

        i = 0
        for card in communityCards:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 200), Card.COMMUNITY_CARD, '', self.communitySprites)

        i = 0
        for card in cardsList:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 450), Card.COMMUNITY_CARD, '', self.communitySprites)

        TextSprite("Gre wygrywa " + player.name, (550, 300), 60, (200, 30, 10), self.communitySprites)
        TextSprite("Nacisnij strzalke w prawo aby rozpoczac nowa runde", (550, 400), 60, (150, 150, 150), self.communitySprites)
        if player.roundResult is not None:
            TextSprite("\""+player.roundResult.resultName+"\"", (550, 360), 50, (200, 40, 200), self.communitySprites)


class Clock:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.addListener(self)
        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            event = ClockEvent()
            self.eventManager.addEventToQueue(event)

    def refresh(self, event):
        if isinstance(event, QuitEvent):
            self.keepGoing = False

def main():
    eventListener = EventListener()
    KeyboardController(eventListener)
    clock = Clock(eventListener)
    PygameView(eventListener)
    Game(eventListener)
    clock.run()


if __name__ == "__main__":
    main()
