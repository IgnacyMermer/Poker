from pygame import *
import pygame
from Events import *
from Components import *

class TextSprite(pygame.sprite.Sprite):

    """
    This class is using Sprite, pygame sublibraly. It allows to display text on the screen and changing its color, position, text and size.
    The function writeSomething is rendering with pygame the changes.
    """

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


class CardSprite(pygame.sprite.Sprite):

    """
    This class is using Sprite, pygame sublibraly. It allows to display card on the screen and changing its position and card image.
    Functions update, getDelX, getDelY allows also for changing position of the card on the screen in slow motion which makes a
    pretty animation. Funtion getCardImageName allows to take the name of the file in images folder and download this image with pygame
    and then display as the card. 
    """

    def __init__(self, card, pos1,  pos2, type, image = '', group=None):
        pygame.sprite.Sprite.__init__(self, group)
        if image == '':
            image = pygame.image.load(self.getCardImageName(card))
        else:
            image = pygame.image.load(image)
        self.srcImage = image
        self.image = self.srcImage
        self.pos = [0.0, 0.0]
        self.pos[0] = pos1[0] * 1.0
        self.pos[1] = pos1[1] * 1.0
        self.pos2 = pos2
        self.pos1 = pos1
        self.type = type
        self.rect = self.srcImage.get_rect()

    def update(self, seconds):
        PLAYER_CARD = 'playerCard'
        COMMUNITY_CARD = 'communityCard'
        if(self.type == PLAYER_CARD or self.type == COMMUNITY_CARD):
            if self.pos2[0] - self.pos1[0] < 0 \
                and self.pos2[0] <= self.pos[0]:
                self.pos[0] += self.getDelX(0.6, seconds)
                if self.pos[0] <= self.pos2[0]:
                    self.pos[0] = self.pos2[0]
            if self.pos2[0] - self.pos1[0] >= 0 \
                and self.pos2[0] >= self.pos[0]:
                self.pos[0] += self.getDelX(0.6, seconds)
                if self.pos[0] >= self.pos2[0]:
                    self.pos[0] = self.pos2[0]
            if self.pos2[1] - self.pos1[1] < 0 \
                and self.pos2[1] <= self.pos[1]:
                self.pos[1] += self.getDelY(0.6, seconds)
                if self.pos[1] <= self.pos2[1]:
                    self.pos[1] = self.pos2[1]
            if self.pos2[1] - self.pos1[1] >= 0 \
                and self.pos2[1] >= self.pos[1]:
                self.pos[1] += self.getDelY(0.6, seconds)
                if self.pos[1] >= self.pos2[1]:
                    self.pos[1] = self.pos2[1]

        self.rect.centerx = round(self.pos[0], 0)
        self.rect.centery = round(self.pos[1], 0)

    def getDelX(self, speed, seconds):
        return (-1.0) *(self.pos1[0] - self.pos2[0]) / seconds / speed

    def getDelY(self, speed, seconds):
        return (-1.0) *(self.pos1[1] - self.pos2[1]) / seconds / speed

    def getCardImageName(self, card):
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

            if rank > 1 and rank <= 10:
                rankStr = str(rank)
            elif rank == 11:
                rankStr = 'jopek'
            elif rank == 12:
                rankStr = 'dama'
            elif rank == 13:
                rankStr = 'krol'
            elif rank == 14:
                rankStr = 'as'

            tempStr = f'images/{rankStr}_{colorStr}.png'
            return tempStr

class TableSprite(pygame.sprite.Sprite):

    """
    This class is using Sprite, pygame sublibraly. It allows to set the background to default.
    """

    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        tableSurf = pygame.Surface((1400, 800))
        tableSurf = tableSurf.convert_alpha()
        tableSurf.fill((0, 0, 0, 0))

        self.image = tableSurf
        self.rect = (0, 0)