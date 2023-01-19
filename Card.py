import random
from pygame import *
from listeners.Events import *
from components.Components import *
from components.Sprites import *


class Card:
    PLAYER_CARD = 'playerCard'
    COMMUNITY_CARD = 'communityCard'
    CARDS_POSITION = [750, 50]

    def __init__(self, color, rank):
        self.color = color
        self.rank = rank

    def getRank(self):
        return self.rank

    def getColor(self):
        return self.color


class GameCards:
    def __init__(self):
        self.gameCards = []

    def initializeCards(self):
        self.gameCards = []

        for i in range(0, 4):
            for j in range(2, 15):
                self.gameCards.append(Card(i, j))

    def mixCards(self):
        mixedCards = []
        for i in range(len(self.gameCards)):
            if len(self.gameCards) > 1:
                tempCard = random.choice(self.gameCards)
                mixedCards.append(tempCard)
                self.gameCards.remove(tempCard)
            else:
                tempCard = self.gameCards.pop()
                mixedCards.append(tempCard)
        self.gameCards = mixedCards

    def popCard(self):
        return self.gameCards.pop()


class Result:
    def __init__(self, resultName, score):
        self.resultName = resultName
        self.score = score


class PokerHandler:
    """
    Below are 7 seven state which describes and tells the app in which moment
    of the game the app is
    """

    ROYAL_POKER = ['Royal_Poker', 10000]
    POKER = ['Poker', 5000]
    CARRIAGE = ['Carriage', 3000]
    FULL = ['Full', 2000]
    COLOR = ['Color', 1000]
    STRIT = ['Strit', 600]

    TRIPLE = ['Triple', 300]
    TWO_PAIR = ['Two_Pair', 200]
    SINGLE_PAIR = ['Single_Pair', 100]

    HIGH_CARD = ['High_Card', 10]

    def __init__(self):
        pass

    @staticmethod
    def compareTwoPlayerCards(player1, player2):
        """
        This function takes two players as parameters and return 1 if first
        player result of the round is higher, returns -1 if 
        second player has higher result and 0 if there is a draw between them.
        """

        result1 = player1.roundResult
        result2 = player2.roundResult
        if result1.score < result2.score:
            return -1
        elif result1.score > result2.score:
            return 1
        else:
            return 0

    @staticmethod
    def isTheSameColor(cards):
        color = cards[0].color
        for card in cards:
            if card.color is not color:
                return False
        return True

    @staticmethod
    def getBestCards(cards):
        """
        This function check how many cards the program passed as the parameter
        and then void returnResult function for every 5 cards 
        in passed cards. Then function returns the best result
        """

        if len(cards) == 5:
            sortedCardsList = []
            for card in cards:
                index = 0
                for tempCard in sortedCardsList:
                    if card.rank > tempCard.rank:
                        index += 1
                sortedCardsList.insert(index, card)
            return PokerHandler.returnResult(sortedCardsList)
        elif len(cards) == 6:
            scoresList = []
            for i in range(0, 6):
                cuttedList = []
                for z in range(0, 6):
                    if z is not i:
                        cuttedList.append(cards[z])
                sortedCardsList = []
                for card in cuttedList:
                    index = 0
                    for tempCard in sortedCardsList:
                        if card.rank > tempCard.rank:
                            index += 1
                    sortedCardsList.insert(index, card)
                scoresList.append(PokerHandler.returnResult(sortedCardsList))
            maxRank = 0
            bestScore = {}
            for score in scoresList:
                if score.score > maxRank:
                    bestScore = score
            return bestScore
        else:
            scoresList = []
            for i in range(0, 6):
                for j in range(i+1, 7):
                    cuttedList = []
                    for z in range(0, 7):
                        if z is not i and z is not j:
                            cuttedList.append(cards[z])
                    sortedCardsList = []
                    for card in cuttedList:
                        index = 0
                        for tempCard in sortedCardsList:
                            if card.rank > tempCard.rank:
                                index += 1
                        sortedCardsList.insert(index, card)

                    scoresList.append(PokerHandler.returnResult(
                                      sortedCardsList))
            maxRank = 0
            bestScore = {}
            for score in scoresList:
                if score.score > maxRank:
                    maxRank = score.score
                    bestScore = score
            return bestScore

    @staticmethod
    def returnResult(sortedCardsList):
        """
        This function checks if sorted cards passed in parameter are any cards
        figure. It returns the result consisting of default
        score value for card figure and extra points for the highest card, but
        this extra points can't exceed next card figure score 
        value in the table.
        """

        if sortedCardsList[0].rank == 10 and sortedCardsList[1].rank == 11 and\
            sortedCardsList[2].rank == 12 and \
            sortedCardsList[3].rank == 13 and sortedCardsList[4].rank == 14 and \
            PokerHandler.isTheSameColor(sortedCardsList):
            return Result(PokerHandler.ROYAL_POKER[0], PokerHandler.ROYAL_POKER[1])
        elif sortedCardsList[4].rank == 14 and PokerHandler.isTheSameColor(sortedCardsList) and \
            sortedCardsList[0].rank == 2 and \
            sortedCardsList[1].rank == 3 and sortedCardsList[2].rank == 4 and \
            sortedCardsList[3].rank == 5:
            return Result(PokerHandler.ROYAL_POKER[0], PokerHandler.ROYAL_POKER[1]-100)
        elif PokerHandler.isTheSameColor(sortedCardsList) and \
            sortedCardsList[1].rank == sortedCardsList[0].rank + 1 and \
            sortedCardsList[2].rank == sortedCardsList[0].rank + 2 and \
            sortedCardsList[3].rank == sortedCardsList[0].rank + 3 and \
            sortedCardsList[4].rank == sortedCardsList[0].rank + 4:
            return Result(PokerHandler.POKER[0], PokerHandler.POKER[1] + sortedCardsList[4].rank * 100)
        elif (sortedCardsList[1].rank == sortedCardsList[0].rank and \
            sortedCardsList[2].rank == sortedCardsList[0].rank and \
            sortedCardsList[3].rank == sortedCardsList[0].rank) or \
            (sortedCardsList[1].rank == sortedCardsList[4].rank and sortedCardsList[2].rank == sortedCardsList[4].rank and \
            sortedCardsList[3].rank == sortedCardsList[4].rank):
            additionalScore = sortedCardsList[2].rank * 80
            if sortedCardsList[0].rank != sortedCardsList[1].rank:
                additionalScore += sortedCardsList[0].rank * 5
            elif sortedCardsList[4].rank != sortedCardsList[3].rank:
                additionalScore += sortedCardsList[4].rank * 5
            return Result(PokerHandler.CARRIAGE[0], PokerHandler.CARRIAGE[1] + additionalScore)
        elif (sortedCardsList[1].rank == sortedCardsList[0].rank and sortedCardsList[2].rank == sortedCardsList[0].rank and \
            sortedCardsList[3].rank == sortedCardsList[4].rank):
            additionalScore = sortedCardsList[0].rank*50 + sortedCardsList[3].rank
            return Result(PokerHandler.FULL[0], PokerHandler.FULL[1] + additionalScore)
        elif (sortedCardsList[2].rank == sortedCardsList[4].rank and sortedCardsList[3].rank == sortedCardsList[4].rank and \
            sortedCardsList[0].rank == sortedCardsList[1].rank):
            additionalScore = sortedCardsList[4].rank*50 + sortedCardsList[1].rank
            return Result(PokerHandler.FULL[0], PokerHandler.FULL[1] + additionalScore)
        elif PokerHandler.isTheSameColor(sortedCardsList):
            additionalScore = sortedCardsList[4].rank * 40 + sortedCardsList[3].rank * 3 + sortedCardsList[2].rank * 0.1
            return Result(PokerHandler.COLOR[0], PokerHandler.COLOR[1] + additionalScore)
        elif sortedCardsList[1].rank == sortedCardsList[0].rank + 1 and \
            sortedCardsList[2].rank == sortedCardsList[0].rank + 2 and sortedCardsList[3].rank == sortedCardsList[0].rank + 3 and \
            sortedCardsList[4].rank == sortedCardsList[0].rank + 4:
            return Result(PokerHandler.STRIT[0], PokerHandler.STRIT[1] + sortedCardsList[4].rank * 10)
        elif sortedCardsList[1].rank == sortedCardsList[0].rank and sortedCardsList[2].rank == sortedCardsList[0].rank:
            return Result(PokerHandler.TRIPLE[0],
                          PokerHandler.TRIPLE[1] + sortedCardsList[1].rank * 10)
        elif sortedCardsList[2].rank == sortedCardsList[4].rank and \
            sortedCardsList[3].rank == sortedCardsList[4].rank:
            return Result(PokerHandler.TRIPLE[0],
                          PokerHandler.TRIPLE[1] + sortedCardsList[2].rank * 10)
        elif sortedCardsList[0].rank == sortedCardsList[1].rank:
            if sortedCardsList[2].rank == sortedCardsList[3].rank:
                additionalScore = sortedCardsList[3].rank * 5 + \
                    sortedCardsList[1].rank * 0.3 + sortedCardsList[4].rank * 0.02
                return Result(PokerHandler.TWO_PAIR[0], 
                              PokerHandler.TWO_PAIR[1] + additionalScore)
            elif sortedCardsList[3].rank == sortedCardsList[4].rank:
                additionalScore = sortedCardsList[3].rank * 5 + \
                    sortedCardsList[1].rank * 0.3 + sortedCardsList[2].rank * 0.02
                return Result(PokerHandler.TWO_PAIR[0],
                              PokerHandler.TWO_PAIR[1] + additionalScore)
            else:
                additionalScore = sortedCardsList[0].rank * 5 +\
                    sortedCardsList[4].rank * 0.3
                return Result(PokerHandler.SINGLE_PAIR[0],
                              PokerHandler.SINGLE_PAIR[1] + additionalScore)
        elif sortedCardsList[1].rank == sortedCardsList[2].rank:
            if sortedCardsList[3].rank == sortedCardsList[4].rank:
                additionalScore = sortedCardsList[4].rank * 5 + \
                    sortedCardsList[2].rank * 0.3 + sortedCardsList[0].rank * 0.02
                return Result(PokerHandler.TWO_PAIR[0],
                              PokerHandler.TWO_PAIR[1] + additionalScore)
            else:
                additionalScore = sortedCardsList[1].rank * 5 + \
                    sortedCardsList[4].rank * 0.3 + sortedCardsList[3].rank * 0.02
                return Result(PokerHandler.SINGLE_PAIR[0],
                              PokerHandler.SINGLE_PAIR[1] + additionalScore)
        elif sortedCardsList[2].rank == sortedCardsList[3].rank:
            additionalScore = sortedCardsList[2].rank * 5 + \
                sortedCardsList[4].rank * 0.3 + sortedCardsList[1].rank * 0.02
            return Result(PokerHandler.SINGLE_PAIR[0],
                          PokerHandler.SINGLE_PAIR[1] + additionalScore)
        elif sortedCardsList[3].rank == sortedCardsList[4].rank:
            additionalScore = sortedCardsList[3].rank * 5 + \
                sortedCardsList[2].rank * 0.3 + sortedCardsList[1].rank * 0.02
            return Result(PokerHandler.SINGLE_PAIR[0],
                          PokerHandler.SINGLE_PAIR[1] + additionalScore)
        else:
            additionalScore = sortedCardsList[4].rank * 5 + \
                sortedCardsList[3].rank * 0.3 + sortedCardsList[2].rank * 0.02
            return Result(PokerHandler.HIGH_CARD[0],
                          PokerHandler.HIGH_CARD[1] + additionalScore)

    @staticmethod
    def getTwoCardResult(cards):
        """
        This function checks if two cards passed as the parameter are pair or
        two different cards and return result for
        these cards.
        """

        if len(cards) != 2:
            raise ValueError("Not two cards passed as the parameter")
        sortedCardsList = []
        for card in cards:  
            index = 0
            for tempCard in sortedCardsList:
                if card.rank > tempCard.rank:
                    index += 1
            sortedCardsList.insert(index, card)
        if sortedCardsList[0].rank == sortedCardsList[1].rank:
            additionalScore = sortedCardsList[1].rank * 5
            return Result(PokerHandler.SINGLE_PAIR[0],
                          PokerHandler.SINGLE_PAIR[1] + additionalScore)
        else:
            return Result(PokerHandler.HIGH_CARD[0],
                          PokerHandler.HIGH_CARD[1] + sortedCardsList[1].rank)
