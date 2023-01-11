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

        

        
    