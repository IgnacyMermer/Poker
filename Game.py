from Card import *
from Components import *
from Sprites import *
from Player import *


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
                    self.players[1].riskLevel > 1 and 35 - player.moneyOnTable <= player.currentMoney:
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
        """
        In this void we check if all players equal their moneyOnTable to highestMoney or they are out of the round. Before this checking
        we call void secondMoney in which we handle second auction in game. After auction we go to Turn state and update players' money display 
        on the screen and show one more community card. If the game is over in this state we go to River state and show cards of the winner. 
        """

        self.secondMoney()
        print(self.checkIfEnd())
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
            print('alal')
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
                            else:
                                highestPrice = price+player.moneyOnTable
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
                if highestPrice < 35 and highestPrice <= player.currentMoney:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 100:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and 45 <= player.currentMoney and \
                                40 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 40
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 38 <= player.currentMoney and \
                                35 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 35
                            elif 35 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 35
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and 50 <= player.currentMoney and \
                                50 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 50
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 45 <= player.currentMoney and \
                                45 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 45
                            elif 40 - player.moneyOnTable <= player.currentMoney:
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
                        if player.riskLevel > 1 and 60 <= player.currentMoney and \
                                60 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 60
                        elif player.riskLevel > 0 and 57 <= player.currentMoney and \
                                52 - player.moneyOnTable <= player.currentMoney:
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
                        if 60 - player.moneyOnTable <= player.currentMoney:
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
        """
        We do the same things as in dealFlop and dealTurn functions. We go to function thirdMoney and handle third auction until 
        all players put the same money as the highest or they resign of the round.
        """

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
                            else:
                                highestPrice = price+player.moneyOnTable
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
                        if player.riskLevel > 1 and 66 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 66
                        elif player.riskLevel > 0 and 60 - player.moneyOnTable <= player.currentMoney:
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
                        if 70 - player.moneyOnTable <= player.currentMoney:
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
                        if 70 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 70
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 2500 and highestPrice <= player.currentMoney:
                        if 75 - player.moneyOnTable <= player.currentMoney:
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
                        if 74 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 74
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3000 and highestPrice <= player.currentMoney:
                        if 79 - player.moneyOnTable <= player.currentMoney:
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
                        if 76 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 76
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 84 - player.moneyOnTable <= player.currentMoney:
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
                        if 82 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 82
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 86 - player.moneyOnTable <= player.currentMoney:
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
                        if 86 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 86
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 6500 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 88 - player.moneyOnTable <= player.currentMoney:
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
                        if 91 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 91
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 7500 and player.riskLevel == 2 and highestPrice <= player.currentMoney:
                        if 94 - player.moneyOnTable <= player.currentMoney:
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
        """
        This function check if in the round is more than one player still playing, if not it return True means that game is over
        """

        countAlive = 0
        for player in self.players:
            if player.currentAlive == 'Alive':
                countAlive += 1
        if countAlive > 1:
            return False
        return True
    
    def showDown(self):
        """
        This function changes state to State Showdown and call showDown event to show winner's cards on the screen. Before that it calls 
        function choiceBestCards which choose the best 5 cards from 7 and assign the result of the round to every player which is still alive
        """

        self.state = Game.STATE_SHOWDOWN
        
        for player in self.players:
            player.choiceBestCards(self.communityCards)
        
        if self.players[0].currentAlive != 'Alive' or self.players[0].moneyOnTable != 0:
            winner = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players, winner, self.communityCards, winner.cards))


    def getWinner(self):
        """
        This function compare all players results and choose the best player in the round. It restarts all player's values to start next round if
        user will want it.  
        """
        
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
            player.roundResult = None
            player.currentAlive = 'Alive'
            player.cards = []

        bestPlayer.currentMoney += allMoneyOnTable
        return bestPlayer