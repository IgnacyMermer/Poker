import pygame
from pygame import *
from Components import *
from Events import *
from Sprites import *
from Card import *


class PygameView:

    """
    This class connects program with pygame. It runs Pygame application, set screen size, title of the program etc. It connects itself with listeners.
    """

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
        self.scoreSprites = []
        self.moneyText = ''


    def refresh(self, event):

        """
        This function allows to handle events if the user click on button or quit the application. It also allows to refresh data on the screen 
        with every clock event. It checks events in eventManager and do adequate updates on the screen to every event.  
        """

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
            firstLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.players[0].currentMoney/2}$) albo pas (p)', (700, 50), 30, (150, 150, 150), self.playerSprites)
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
            secondLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.playersList[0].currentMoney}$) albo pas (p)', (700, 50), 30, (150, 150, 150), self.playerSprites)
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
            thirdLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.playersList[0].currentMoney}$) albo pas (p)', (700, 50), 30, (150, 150, 150), self.playerSprites)
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
            thirdLicitacja = TextSprite(f'Podaj kwote licytacji (1$ - {event.playersList[0].currentMoney}$) albo pas (p)', (700, 50), 30, (150, 150, 150), self.playerSprites)
            self.betsSprites.append(thirdLicitacja)
            self.showRiverCard(event.card, event.playersList)

        if isinstance(event, ShowDownEvent):
            print(event.cardList)
            print('----')
            self.showDownResult(event.players, event.player, event.communityCards, event.cardList)

    def showPreFlopCards(self, players):

        """
        This function shows two cards to every player, but user see only its cards, other players' cards are hidden
        """

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

        """
        This function shows 3 community cards in the centre of the screen
        """

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
                self.scoreSprites.append(TextSprite(str(player.moneyOnTable), (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
            else:
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite(str(player.moneyOnTable), (POS_LEFT + 40, POS_TOP - 20), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite('Poza runda', (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
        i = 0
        for card in cardList:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 350), Card.COMMUNITY_CARD, '', self.communitySprites)

    def showTurnCard(self, card, players):

        """
        This function shows 1 more community card in the same row as the previous cards
        """

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
                self.scoreSprites.append(TextSprite(str(player.moneyOnTable), (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
            else:
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite(str(player.moneyOnTable), (POS_LEFT + 40, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite('Poza runda', (POS_LEFT + 30, POS_TOP - 20), 30, (150, 150, 150), self.playerSprites))
        CardSprite(card, Card.CARDS_POSITION, (750, 350), Card.COMMUNITY_CARD, '', self.communitySprites)

    def showRiverCard(self, card, players):
        
        """
        This function shows the fifth community card in the same row as the previous cards, this is the last community card
        """

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
                self.scoreSprites.append(TextSprite(str(player.moneyOnTable), (POS_LEFT + 30, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
            else:
                self.scoreSprites.append(TextSprite(str(player.currentMoney), (POS_LEFT + 40, POS_TOP - 80), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite(str(player.moneyOnTable), (POS_LEFT + 40, POS_TOP - 50), 30, (150, 150, 150), self.playerSprites))
                self.scoreSprites.append(TextSprite('Poza runda', (POS_LEFT + 30, POS_TOP - 20), 30, (150, 150, 150), self.playerSprites))
        CardSprite(card, Card.CARDS_POSITION, (850, 350), Card.COMMUNITY_CARD, '', self.communitySprites)
    
    def showDownResult(self, players, player, communityCards, cardsList):

        """
        This function clear the screen from previous cards and display who is the winner and what cards the winner has
        """

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
        print(cardsList)
        for card in communityCards:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 380), Card.COMMUNITY_CARD, '', self.communitySprites)

        i = 0
        for card in cardsList:
            i += 1
            CardSprite(card, Card.CARDS_POSITION, (350 + i * 100, 640), Card.COMMUNITY_CARD, '', self.communitySprites)

        TextSprite("Gre wygrywa " + player.name, (550, 150), 60, (200, 30, 10), self.communitySprites)
        TextSprite("Nacisnij strzalke w prawo aby rozpoczac nowa runde", (550, 200), 60, (150, 150, 150), self.communitySprites)
        if player.roundResult is not None:
            TextSprite("\""+player.roundResult.resultName+"\"", (550, 260), 50, (200, 40, 200), self.communitySprites)