import pygame


class Button:
    def __init__(self, imageUrl, x, y, screen):
        image = pygame.image.load(imageUrl).convert_alpha()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = ((x-self.image.get_width())/2, y)

        screen.blit(self.image, ((x-self.image.get_width())/2, y))


    def onClick(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

        return False

        

class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = width
        self.font = pygame.font.SysFont(None, 100)
        self.text = ""
        self.renderText()

    def renderText(self):
        fontText = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, fontText.get_width()+10), fontText.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(fontText, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.renderText()

    def getText(self):
        return self.text
    