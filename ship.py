import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.moving_right = False
        
        self.image = pygame.image.load('models\spaceship_0.png')
        self.rect = self.image.get_rect()
        
        self.rect.midbottom = self.screen_rect.midbottom
    
    def update(self):
        if self.moving_right:
            self.rect.x += 1
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)