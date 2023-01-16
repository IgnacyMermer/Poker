class Event:

    def __init__(self):
        self.name = "Jakis event"


class GameStartEvent(Event):
    def __init__(self, playersCount):
        self.name = "The game started"
        self.playersCount = playersCount


class ClockEvent(Event):
    def __init__(self):
        self.name = "Clock tick event"


class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit event"


class NextMoveEvent(Event):
    def __init__(self):
        self.name = "Next move event"


class PreFlopEvent(Event):
    def __init__(self, players):
        self.name = "Pre-Flop Event"
        self.players = players


class FlopEvent(Event):
    def __init__(self, cardList, playersList):
        self.name = "Flop Event"
        self.cardList = cardList
        self.playersList = playersList


class TurnEvent(Event):
    def __init__(self, card, playersList):
        self.name = "Turn Event"
        self.card = card
        self.playersList = playersList


class RiverEvent(Event):
    def __init__(self, card, playersList):
        self.name = "Flop Event"
        self.card = card
        self.playersList = playersList


class ShowDownEvent(Event):
    def __init__(self, players, player, communityCards, cardList):
        self.name = "Show down event"
        self.player = player
        self.players = players
        self.communityCards = communityCards
        self.cardList = cardList


class MoneyTextEvent(Event):
    def __init__(self, text, maxPrice=0):
        self.name = "Money Text event"
        self.text = text


class MoneyToEquals(Event):
    def __init__(self, text, maxPrice=0):
        self.name = "Money To Equals event"
        self.maxPrice = maxPrice
        self.text = text


class ClearMoneyEvent(Event):
    def __init__(self):
        self.name = "Clear money event"
