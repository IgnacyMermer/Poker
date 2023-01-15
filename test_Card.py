from Card import *
from Player import *

def test_sortedCards():
    """Not working, it was made while getBestCard function was created"""
    card1 = Card('serce', 10)
    card2 = Card('serce', 11)
    card3 = Card('serce', 9)
    assert PokerHandler.GetBestChoise([card1, card2, card3]) == [card3, card1, card2]

def test_royalPoker():
    """For seven cards"""
    assert PokerHandler.getBestCards([Card('serce', 4), Card('serce', 3), Card('serce', 6), Card('serce', 8), Card('zoladz', 7), Card('serce', 2), Card('serce', 5)]).resultName == 'Poker'
    assert PokerHandler.getBestCards([Card('serce', 4), Card('serce', 3), Card('serce', 14), Card('serce', 8), Card('serce', 7), Card('serce', 2), Card('serce', 5)]).resultName == 'Royal_Poker'
    assert PokerHandler.getBestCards([Card('serce', 8), Card('wino', 7), Card('serce', 9), Card('dzwonek', 11), Card('zoladz', 10), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Strit'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('serce', 3), Card('serce', 5), Card('serce', 2), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Color'
    assert PokerHandler.getBestCards([Card('serce', 8), Card('serce', 7), Card('serce', 9), Card('serce', 6), Card('serce', 10), Card('dzwonek', 4), Card('zoladz', 10)]).resultName == 'Poker'
    assert PokerHandler.getBestCards([Card('dzwonek', 10), Card('wino', 6), Card('serce', 10), Card('zoladz', 3), Card('wino', 11), Card('wino', 2), Card('zoladz', 5)]).resultName == 'Single_Pair'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('serce', 13), Card('serce', 14), Card('wino', 14), Card('serce', 13), Card('dzwonek', 5), Card('zoladz',7)]).resultName == 'Two_Pair'
    assert PokerHandler.getBestCards([Card('wino', 12), Card('serce', 12), Card('wino', 11), Card('serce', 11), Card('dzwonek', 11), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Full'
    assert PokerHandler.getBestCards([Card('serce', 9), Card('serce', 10), Card('serce', 13), Card('wino', 13), Card('dzwonek', 13), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Triple'
    assert PokerHandler.getBestCards([Card('serce', 11), Card('serce', 10), Card('serce', 12), Card('serce', 14), Card('serce', 13), Card('dzwonek', 3), Card('zoladz', 6)]).resultName == 'Royal_Poker'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('wino', 9), Card('serce', 11), Card('serce', 13), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Strit'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('serce', 3), Card('serce', 11), Card('serce', 13), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Color'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('serce', 9), Card('serce', 11), Card('serce', 8), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Poker'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('wino', 9), Card('serce', 11), Card('serce', 2), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Single_Pair'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Two_Pair'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Full'
    assert PokerHandler.getBestCards([Card('serce', 9), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11), Card('dzwonek', 2), Card('zoladz', 5)]).resultName == 'Triple'

    """For six cards"""
    assert PokerHandler.getBestCards([Card('serce', 10), Card('wino', 9), Card('zoladz', 10), Card('serce', 2), Card('serce', 12), Card('serce', 5)]).resultName == 'Single_Pair'
    assert PokerHandler.getBestCards([Card('zoladz', 10), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('serce', 12), Card('serce', 5)]).resultName == 'Two_Pair'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('zoladz', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11), Card('serce', 5)]).resultName == 'Full'
    assert PokerHandler.getBestCards([Card('serce', 9), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11), Card('serce', 5)]).resultName == 'Triple'

    """For five cards"""
    assert PokerHandler.getBestCards([Card('serce', 10), Card('wino', 9), Card('zoladz', 10), Card('serce', 2), Card('serce', 12)]).resultName == 'Single_Pair'
    assert PokerHandler.getBestCards([Card('zoladz', 10), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('serce', 12)]).resultName == 'Two_Pair'
    assert PokerHandler.getBestCards([Card('serce', 10), Card('zoladz', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11)]).resultName == 'Full'
    assert PokerHandler.getBestCards([Card('serce', 9), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11)]).resultName == 'Triple'


def test_compareTwoPlayersResults():
    player1 = Player('jeden', 0)
    player1.roundResult = PokerHandler.getBestCards([Card('serce', 10), Card('wino', 9), Card('zoladz', 10), Card('serce', 2), Card('serce', 12)])
    player2 = Player('dwa', 0)
    player2.roundResult = PokerHandler.getBestCards([Card('serce', 10), Card('zoladz', 10), Card('serce', 11), Card('wino', 11), Card('zoladz', 11)])
    assert PokerHandler.compareTwoPlayerCards(player1, player2) == -1


def test_getTwoCardResult():
    assert PokerHandler.getTwoCardResult([Card('serce', 2), Card('zoladz', 2)]).resultName == 'Single_Pair'
    assert PokerHandler.getTwoCardResult([Card('serce', 3), Card('serce', 2)]).resultName == 'High_Card'
    assert PokerHandler.getTwoCardResult([Card('dzwonek', 10), Card('wino', 10)]).resultName == 'Single_Pair'
    assert PokerHandler.getTwoCardResult([Card('serce', 3), Card('serce', 8)]).resultName == 'High_Card'
    assert PokerHandler.getTwoCardResult([Card('serce', 12), Card('zoladz', 12)]).resultName == 'Single_Pair'
    assert PokerHandler.getTwoCardResult([Card('serce', 5), Card('serce', 2)]).resultName == 'High_Card'


def test_creatingPlayer():
    player = Player('myName', 0)
    assert player.name == 'myName'
    assert player.riskLevel == 1
    assert player.cards == []
    player.addCards(Card('serce', 3))
    assert len(player.cards) == 1
    assert player.cards[0].color == 'serce'
    assert player.cards[0].rank == 3
