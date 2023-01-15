from CardFile import *

def test_sortedCards():
    card1 = Card('czerwien', 10)
    card2 = Card('czerwien', 11)
    card3 = Card('czerwien', 9)
    assert PokerHandler.GetBestChoise([card1, card2, card3]) == [card3, card1, card2]

def test_royalPoker():
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('serce', 9), Card('serce', 11), Card('serce', 13), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Royal_Poker'
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('wino', 9), Card('serce', 11), Card('serce', 13), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Strit'
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('serce', 3), Card('serce', 11), Card('serce', 13), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Color'
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('serce', 9), Card('serce', 11), Card('serce', 8), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Poker'
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('wino', 9), Card('serce', 11), Card('serce', 2), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'High_Card'
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('serce', 12), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Two_Pair'
    assert PokerHandler.GetBestChoice([Card('serce', 10), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('serce', 11), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Full'
    assert PokerHandler.GetBestChoice([Card('serce', 9), Card('serce', 10), Card('serce', 11), Card('wino', 11), Card('serce', 11), Card('dzwonek', 2), Card('zoladz', 5)]).result_name == 'Triple'