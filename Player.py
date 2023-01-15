from Card import *


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

    def choiceBestCards(self, communityCards):
        """This function void another functions which join user's cards and community's cards and choice the best 5 cards from seven and return result, 
        which is set to roundResult variable
        """

        tempList = self.cards + communityCards
        result = PokerHandler.getBestCards(tempList)
        self.roundResult = result
