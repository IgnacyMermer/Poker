from Card import GameCards
from components.Components import *
from components.Sprites import *
from Player import Player
from random import randint
from listeners.Events import MoneyTextEvent, GameStartEvent, MoneyToEquals,\
                   NextMoveEvent, ClearMoneyEvent, PreFlopEvent, FlopEvent,\
                   TurnEvent, RiverEvent, ShowDownEvent
from auctions.Auction4 import FourthAuction
from auctions.Auction3 import ThirdAuction
from auctions.Auction2 import SecondAuction
from auctions.Auction1 import FirstAuction


class Game:
    """
    This class is responsible for managing the entire game. It contains 7 
    states which tells program, in which moment of the game we are. 
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
        eventManager is to add class' listener to it. It allows to call
        refresh funtion on every clock tick and check events and game states,
        call another function on every moment of the game. In initial state it
        set game state on STATE_START, it call start function.
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
            if self.myName == "":
                self.myName = "Default name"
            if event.playersCount != -1:
                self.playersCount = 1 + event.playersCount
                if self.state == Game.STATE_START:
                    self.start(event.level)
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

    def start(self, level):
        self.initializePlayers(level)
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

    def initializePlayers(self, level):
        self.players = []
        self.players.append(Player(self.myName, 0, 0))
        nameList = ['Zdzichu', 'Zbychu', 'Damcio', 'Pawcio']
        for i in range(1, self.playersCount):
            playerLevel = 2
            if level < 3:
                if level == 2:
                    playerLevel = 1
                else:
                    if i % 2 == 0:
                        playerLevel = 1
                    else:
                        playerLevel = 0
            self.players.append(Player(nameList[i], i, playerLevel))

    def dealPreflop(self):
        """
        In this moment of game, players get two first cards and 
        then they start auction
        """

        self.state = Game.STATE_PREFLOP
        playerCount = len(self.players)

        for i in range(playerCount * 2):
            self.players[i % playerCount].addCards(self.gameCards.popCard())

        self.eventManager.addEventToQueue(PreFlopEvent(self.players))

    def dealFlop(self):

        """
        Here is call function (firstMoney) responds for handling first auction
        in round, then computer shows 3 community cards.
        """

        returnValues = FirstAuction.firstMoney(self.isFirstTime,
                                               self.highestMoney, self.players,
                                               self.communityCards,
                                               self.moneyText)
        self.isFirstTime = returnValues[1]
        self.highestMoney = returnValues[0]
        self.players = returnValues[2]

        if not self.checkIfEnd():
            tempBool = True
            self.eventManager.addEventToQueue(ClearMoneyEvent())
            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and \
                   self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                self.state = Game.STATE_FLOP
                for i in range(3):
                    self.communityCards.append(self.gameCards.popCard())

                self.isFirstTime = True
                self.eventManager.addEventToQueue(FlopEvent(
                                                        self.communityCards,
                                                        self.players))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_RIVER
            playerAlive = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players,
                                                            playerAlive,
                                                            self.communityCards,
                                                            playerAlive.cards))

    def dealTurn(self):
        """
        In this void we check if all players equal their moneyOnTable to
        highestMoney or they are out of the round. Before this checking
        we call void secondMoney in which we handle second auction in game.
        After auction we go to Turn state and update players' money display
        on the screen and show one more community card. If the game is over in
        this state we go to River state and show cards of the winner.
        """

        returnValues = SecondAuction.secondMoney(self.isFirstTime,
                                                 self.highestMoney,
                                                 self.players,
                                                 self.communityCards,
                                                 self.moneyText)
        self.isFirstTime = returnValues[1]
        self.highestMoney = returnValues[0]
        self.players = returnValues[2]

        if not self.checkIfEnd():
            self.eventManager.addEventToQueue(ClearMoneyEvent())

            tempBool = True
            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and \
                   self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                for player in self.players:
                    (player.name+' '+player.currentAlive)
                self.state = Game.STATE_TURN
                tempCards = self.gameCards.popCard()
                self.communityCards.append(tempCards)

                self.isFirstTime = True
                self.eventManager.addEventToQueue(TurnEvent(tempCards, 
                                                            self.players))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_RIVER
            playerAlive = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players,
                                                            playerAlive,
                                                            self.communityCards,
                                                            playerAlive.cards))

    def dealRiver(self):
        """
        We do the same things as in dealFlop and dealTurn functions. We go to
        function thirdMoney and handle third auction until
        all players put the same money as the highest or they resign of the
        round.
        """

        returnValues = ThirdAuction.thirdMoney(self.isFirstTime,
                                               self.highestMoney,
                                               self.players,
                                               self.communityCards,
                                               self.moneyText)
        self.isFirstTime = returnValues[1]
        self.highestMoney = returnValues[0]
        self.players = returnValues[2]

        if not self.checkIfEnd():

            self.eventManager.addEventToQueue(ClearMoneyEvent())

            tempBool = True

            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and \
                   self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                for player in self.players:
                    (player.name+' '+player.currentAlive)
                self.state = Game.STATE_RIVER
                tempCards = self.gameCards.popCard()
                self.communityCards.append(tempCards)

                self.isFirstTime = True
                self.eventManager.addEventToQueue(RiverEvent(tempCards,
                                                             self.players))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_RIVER
            playerAlive = self.getWinner()
            self.eventManager.addEventToQueue(ShowDownEvent(self.players,
                                                            playerAlive,
                                                            self.communityCards,
                                                            playerAlive.cards))

    def checkIfEnd(self):
        """
        This function check if in the round is more than one player still
        playing, if not it return True means that game is over
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
        This function changes state to State Showdown and call showDown event
        to show winner's cards on the screen. Before that it calls
        function choiceBestCards which choose the best 5 cards from 7 and
        assign the result of the round to every player which is still alive
        """

        returnValues = FourthAuction.fourthMoney(self.isFirstTime,
                                                 self.highestMoney,
                                                 self.players,
                                                 self.communityCards,
                                                 self.moneyText)
        self.isFirstTime = returnValues[1]
        self.highestMoney = returnValues[0]
        self.players = returnValues[2]

        if not self.checkIfEnd():

            self.eventManager.addEventToQueue(ClearMoneyEvent())

            tempBool = True

            for i in range(len(self.players)):
                if self.players[i].moneyOnTable != self.highestMoney and \
                   self.players[i].currentAlive != 'OOTR':
                    tempBool = False
            if tempBool:
                self.state = Game.STATE_SHOWDOWN

                for player in self.players:
                    player.choiceBestCards(self.communityCards)

                if self.players[0].currentAlive != 'Alive' or \
                   self.players[0].moneyOnTable != 0:
                    winner = self.getWinner()
                    self.eventManager.addEventToQueue(ShowDownEvent(
                                                        self.players, winner,
                                                        self.communityCards,
                                                        winner.cards))
            else:
                self.eventManager.addEventToQueue(MoneyToEquals(f'Podaj kwote ktora chcesz polozyc na stol ({self.highestMoney-self.players[0].moneyOnTable}$ - {50-self.players[0].moneyOnTable}$) albo wyrownaj(w) albo pas(p)',
                        str(self.highestMoney)))
        else:
            self.state = Game.STATE_SHOWDOWN

            for player in self.players:
                player.choiceBestCards(self.communityCards)

            if self.players[0].currentAlive != 'Alive' or \
               self.players[0].moneyOnTable != 0:
                winner = self.getWinner()
                self.eventManager.addEventToQueue(ShowDownEvent(self.players,
                                                                winner,
                                                                self.communityCards,
                                                                winner.cards))

    def getWinner(self):
        """
        This function compare all players results and choose the best player
        in the round. It restarts all player's values to start next round if
        user will want it.
        """

        bestScore = 0
        bestPlayer = None
        allMoneyOnTable = 0

        for player in self.players:
            if player.roundResult is not None:
                if player.roundResult.score > bestScore and \
                   player.currentAlive == 'Alive':
                    bestScore = player.roundResult.score
                    bestPlayer = player
            else:
                if player.currentAlive == 'Alive' and bestScore == 0:
                    bestPlayer = player
        if bestPlayer is None:
            for player in self.players:
                if player.roundResult is not None:
                    if player.roundResult.score > bestScore:
                        bestScore = player.roundResult.score
                        bestPlayer = player
        if bestPlayer is None:
            bestPlayer = self.players[randint(0, len(self.players))]

        copiedBestPlayer = Player(bestPlayer.name, bestPlayer.position,
                                  bestPlayer.riskLevel)
        copiedBestPlayer.cards = bestPlayer.cards
        copiedBestPlayer.roundResult = bestPlayer.roundResult
        copiedBestPlayer.moneyOnTable = bestPlayer.moneyOnTable
        copiedBestPlayer.currentMoney = bestPlayer.currentMoney
        copiedBestPlayer.currentAlive = bestPlayer.currentAlive

        for player in self.players:
            allMoneyOnTable += player.moneyOnTable
            player.moneyOnTable = 0
            player.roundResult = None
            player.currentAlive = 'Alive'
            player.cards = []
        for player in self.players:
            if player.position == bestPlayer.position:
                player.currentMoney += allMoneyOnTable
        # bestPlayer.currentMoney += allMoneyOnTable
        return copiedBestPlayer
