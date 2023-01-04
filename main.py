import pygame
from pygame import *
from Events import *
from Card import *



class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.cards = []
        self.roundResult = None
        self.currentMoney = 100
        self.currentAlive = "Alive"
        self.riskLevel = 1

    def addCards(self, aCard):
        self.cards.append(aCard)
    
    def initCards(self):
        self.cards = []


class Game:
    def __init__(self, eventManager, playersCount):
        self.gameCards = GameCards()
        self.playersCount = playersCount
        self.players = []
        self.communityCards = []

        self.eventManager = eventManager
        self.eventManager.addListener(self)

        self.playerSprites = pygame.sprite.RenderUpdates()


    def start(self):
        pass



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

class KeyboardController:

    def __init__(self, eventManager, playerName=None):
        self.eventManager = eventManager
        self.eventManager.addListener(self)

    def refreshListener(self, event):
        for event in pygame.event.get():
            ev = None
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN \
                    and event.key == pygame.K_ESCAPE:
                pass

            elif event.type == pygame.KEYDOWN \
                    and event.key == (pygame.K_DOWN or pygame.K_UP \
                         or pygame.K_LEFT or pygame.K_RIGHT):
                pass

            elif event.type == pygame.KEYDOWN \
                    and event.key == pygame.K_SPACE:
                pass

class PygameView:

    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.removeListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption('Poker')
        self.background = pygame.Surface(self.window.get_size())


class Clock:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.removeListener(self)
        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            pass

def main():
    """print('Podaj swoje imie:')
    name = input()
    print('Z iloma graczami chcesz grać (1-4)')
    playersCount = input()
    try:
        playersCount = int(playersCount)
        if playersCount < 1 or playersCount > 4:
            raise ValueError('Niepoprawna liczba przeciwników')
    except:
        raise TypeError('Nie została prawidłowo podana liczba graczy')"""
    eventListener = EventListener()

    keybd = KeyboardController(eventListener)
    clock = Clock(eventListener)
    
    pygameView = PygameView(eventListener)
    texas_holdem = Game(eventListener, 4)
    clock.run()


if __name__ == "__main__":
    main()