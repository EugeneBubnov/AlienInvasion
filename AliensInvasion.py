import sys
import pygame
from settings import settings
from ship import *
from bullet import Bullet

# Класс для управления ресурсами и поведением игры
class AlienInvasion:
    # Инициализация игры и создание ресурсов
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Alien Invasion')
        self.settings = settings()

        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.ship = Ship(self)

        self.backgroud_image = pygame.image.load('models\\background_1.png')
        
       # self.bullets = pygame.sprite.Group  
               
    #def _fire_bullet(self):
       # new_bullet = Bullet(self)
       # self.bullets.add(new_bullet)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Переместить корабль вправо
            self.ship.moving_right = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                 # move to left
                    self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
       # elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = False
               
    def _check_events(self):
        # Чтение событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()   
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)           
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _update_screen(self):
            #self.screen.fill(self.settings.bg_color)
            self.screen.blit(self.backgroud_image, (0, 0))
            self.ship.blitme()
            
            pygame.display.flip() 
                 
    def run_game(self):
        # Запуск основного цикла игры
        while(True):
            self._check_events()
            self.ship.update()
           # self.bullets.update()
            self._update_screen()

                        
if __name__ == '__main__':
    #Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()