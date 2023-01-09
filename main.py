import pygame
from pygame import *
from Events import *
from Card import *



class Player:
    def __init__(self, name, position, level = 1):
        self.name = name
        self.position = position
        self.cards = []
        self.roundResult = None
        self.currentMoney = 100
        self.moneyOnTable = 0
        self.currentAlive = "Alive"
        self.riskLevel = level

    def addCards(self, aCard):
        self.cards.append(aCard)
    
    def initCards(self):
        self.cards = []

    def choiceBestCards(self, communityCards):
        tempList = self.cards + communityCards
        result = PokerHandler.getBestCards(tempList)
        self.roundResult = result

class Game:

    STATE_START = 'start'
    STATE_PREPARING = 'preparing'
    STATE_PREFLOP = 'preflop'
    STATE_FLOP = 'flop'
    STATE_TURN = 'turn'
    STATE_RIVER = 'river'
    STATE_SHOWDOWN = 'showdown'


    def __init__(self, eventManager, playersCount, myName):
        self.gameCards = GameCards()
        self.playersCount = playersCount
        self.myName = myName

        self.eventManager = eventManager
        self.eventManager.addListener(self)

        self.playerSprites = pygame.sprite.RenderUpdates()
        self.state = Game.STATE_START



    def refresh(self, event):
        if isinstance(event, GameStartEvent):
            if self.state == Game.STATE_START:
                self.start()
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

    def start(self):
        self.initializePlayers()
        self.initializeRound()
    

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
        self.state = Game.STATE_PREFLOP
        playerCount = len(self.players)

        for i in range(playerCount * 2):
            self.players[i%playerCount].addCards(self.gameCards.popCard())

        self.eventManager.addEventToQueue(PreFlopEvent(self.players))
    
    def dealFlop(self):
        
        self.firstMoney()
        
        for player in self.players:
            print(player.name+' '+player.currentAlive)
        self.state = Game.STATE_FLOP
        for i in range(3):
            self.communityCards.append(self.gameCards.popCard())

        self.eventManager.addEventToQueue(FlopEvent(self.communityCards, self.players))
    
    def firstMoney(self):
        isFirstTime = True
        highestPrice = 0
        while True:
            price = 0
            if isFirstTime:
                player = self.players[0]
                print('Podaj kwote licytacji (1$ - 50$)')
                kwota = input()
                try:
                    price = int(kwota)
                    highestPrice = price
                    player.currentMoney -= price
                    player.moneyOnTable += price
                    if price > 50 or price < 1:
                        raise ValueError('Niepoprawna wartość kwoty licytacji')
                except:
                    raise TypeError('Nie została prawidłowo podana kwota licytacji')
            else:
                player = self.players[0]
                if player.moneyOnTable < highestPrice:
                    print('Najwyzsza stawka na stole: '+str(highestPrice))
                    print(f'Podaj kwote ktora chcesz polozyc na stol ({highestPrice-player.moneyOnTable}$ - {50-player.moneyOnTable}$) albo wyrownaj(w) albo pas(p)')
                    kwota = input()
                    if kwota == 'p':
                        player.currentAlive = 'OOTR'
                    elif kwota == 'w':
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        try:
                            price = int(kwota)
                            if price > 50 or price < 1:
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
            isFirstTime = False
            for i in range(1, len(self.players)):
                player = self.players[i]
                if player.currentAlive == 'Alive' and highestPrice > player.moneyOnTable:
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
            if highestPrice == self.players[0].moneyOnTable or self.players[0].currentAlive != 'Alive':
                self.highestMoney = highestPrice
                break
    
    def dealTurn(self):
        pass

    
    def dealRiver(self):
        pass
    
    def showDown(self):
        pass

    def getWinner(self):
        pass



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

        if self.canMove:
            self.rect.centerx += 100 / seconds
            if self.rect.centerx >= self.prev_x_pos + 100:
                self.ChangeMoveTo()

        if self.canMakeBiggerFont:
            self.DoBiggerEffect(seconds)


class CardSprite(pygame.sprite.Sprite):

    def __init__(self, card, pos1,  pos2, type, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.src_image = pygame.image.load(self.GetCardImageName(card))
        self.image = self.src_image
        self.pos = [0.0, 0.0]
        self.pos[0] = pos1[0] * 1.0  # float
        self.pos[1] = pos1[1] * 1.0  # float
        self.pos2 = pos2
        self.pos1 = pos1
        self.type = type
        self.rect = self.src_image.get_rect()

    def update(self, seconds):
        # updated position over the destination pos
        # calibrate the final pos not over the dest_pos
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

            tmp_str = f'images/{rankStr}_{colorStr}.png'
            return tmp_str

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
                        and event.key == (pygame.K_DOWN or pygame.K_UP \
                            or pygame.K_LEFT or pygame.K_RIGHT):
                    ev = NextMoveEvent()

                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_SPACE:
                    ev = GameStartEvent()
                if ev:
                    self.eventManager.addEventToQueue(ev)


class TableSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        tableSurf = pygame.Surface((1300, 700))
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
        textSurf = font.render("Naciśnij spacje aby rozpoczac", True, (150, 150, 150))
        textSurf = textSurf.convert_alpha()
        self.window.blit(textSurf, (400, 270))

        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.playerSprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()

    def refresh(self, event):
        if isinstance(event, ClockEvent):
            
            
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
            TableSprite(self.backSprites)

        if isinstance(event, PreFlopEvent):
            self.showPreFlopCards(event.players)

        if isinstance(event, FlopEvent):
            self.showCommunityCards(event.cardList, event.playersList)

        if isinstance(event, TurnEvent):
            self.showTurnCard(event.card, event.playersList)

        if isinstance(event, RiverEvent):
            self.showRiverCard(event.card, event.playersList)

        if isinstance(event, ShowDownEvent):
            self.showDownResult(event.player, event.communityCards, event.cardList)
    
    def showPreFlopCards(self, players):

        POS_LEFT = 0
        POS_TOP = 0

        for player in players:
            player_pos = player.position

            if player_pos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif player_pos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif player_pos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif player_pos == 3:
                POS_LEFT = 1150
                POS_TOP = 210

            CardSprite(player.cards[0], Card.CARDS_POSITION, (POS_LEFT - 85, POS_TOP), Card.PLAYER_CARD, self.playerSprites)
            CardSprite(player.cards[1], Card.CARDS_POSITION, (POS_LEFT + 14, POS_TOP), Card.PLAYER_CARD, self.playerSprites)
            TextSprite(player.name, (POS_LEFT - 20, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites)


    def showCommunityCards(self, card_list, players):
        self.scoreSprites = []
        for player in players:
            player_pos = player.position
            POS_LEFT = 0
            POS_TOP = 0

            if player_pos == 0:
                POS_LEFT = 285
                POS_TOP = 210
            elif player_pos == 1:
                POS_LEFT = 220
                POS_TOP = 500
            elif player_pos == 2:
                POS_LEFT = 1220
                POS_TOP = 500
            elif player_pos == 3:
                POS_LEFT = 1150
                POS_TOP = 210

            self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 30, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))

        global isWaitingForInput

        i = 0
        for card in card_list:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 350), Card.COMMUNITY_CARD, self.communitySprites)

    

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
    texas_holdem = Game(eventListener, 4, 'myName')
    clock.run()


if __name__ == "__main__":
    main()